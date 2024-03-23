# Example File
import io

import librosa
import mlflow.keras
import mlflow.tensorflow
import numpy as np
import pandas as pd
from mlflow.models import infer_signature
from prefect import flow, task
from prefect.filesystems import RemoteFileSystem
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

import mlflow

mlflow.set_experiment("LSTM")
remote_file_system_block = RemoteFileSystem.load("data")


@task
def read_dataset(path):
    def read_lines(lines):
        is_header = True
        for line in lines:
            if is_header:
                is_header = False
                continue

            if not line or line.isspace():
                is_header = True
                continue

            label, comment = line.split(maxsplit=1)
            yield comment, int(label)

    with open(path) as file:
        data = read_lines(file)
        df = pd.DataFrame.from_records(data, columns=["text", "label"])

    return df


def _reader_file_content(file_path: str):
    file_content = remote_file_system_block.read_path(file_path)
    buffer = io.BytesIO(file_content)
    return buffer


def features_extractor(file: str):
    audio, sample_rate = librosa.load(_reader_file_content(file))
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    return mfccs_scaled_features


@task()
def get_metadata(metadata_path: str) -> pd.DataFrame:
    file_content = remote_file_system_block.read_path(metadata_path)
    buffer = io.BytesIO(file_content)
    metadata = pd.read_excel(buffer, sheet_name="read_dataset")
    return metadata


@task()
def feature_extractor(
    metadata: pd.DataFrame, violence_dir: str, non_violence_dir: str
) -> pd.DataFrame:
    extracted_features: list = []

    # Extracting features from violent audio
    for record in metadata.values:
        file_name = violence_dir + record[0] + "_violence.wav"
        final_class_label = 1
        try:
            data = features_extractor(file_name)
            extracted_features.append([data, final_class_label])
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")

    # Extracting features from non-violent audio
    for record in metadata.values:
        file_name = non_violence_dir + record[0] + "_non_violence.wav"
        final_class_label = 0
        try:
            data = features_extractor(file_name)
            extracted_features.append([data, final_class_label])
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")

    return pd.DataFrame(extracted_features, columns=["features", "class"])


@task
def split_data(df, test_size):
    x_raw = np.array(df["features"].tolist())
    y = np.array(df["class"].tolist())
    x_train, x_test, y_train, y_test = train_test_split(
        x_raw, y, test_size=test_size, random_state=42
    )
    return x_train, x_test, y_train, y_test


@flow(log_prints=True)
def train():
    # Enable autologging
    mlflow.sklearn.autolog()

    # Load metadata
    metadata = get_metadata(metadata_path="/raw/VSD.xlsx")

    # Extract features
    df = feature_extractor(
        metadata,
        violence_dir="processed/violence_data/",
        non_violence_dir="processed/no_violence_data/",
    )

    # Display dataframe tail and class value counts
    print("Tail of dataframe:")
    print(df.tail())
    print("Class value counts:")
    print(df["class"].value_counts())

    # Split data into train and test sets
    test_size = 0.1
    x_train, x_test, y_train, y_test = split_data(df, test_size)

    print("Train and test data shapes:")
    print(x_train.shape, x_test.shape)

    # Reshaping to make the datasets compatible with LSTM.
    x_train = x_train.reshape(x_train.shape[0], 1, 40)
    x_test = x_test.reshape(x_test.shape[0], 1, 40)
    print(x_train.shape, x_test.shape)

    # Start MLflow run

    with mlflow.start_run() as run:
        mlflow.log_param("test_size", test_size)

        # Define model architecture
        model = Sequential(
            [LSTM(64, input_shape=(1, 40)), Dense(32), Dense(1, activation="sigmoid")]
        )
        print("Model summary:")
        model.summary()

        # Compile model
        print("Compiling model...")
        model.compile(
            loss="binary_crossentropy", metrics=["accuracy"], optimizer="adam"
        )

        num_epochs = 10
        num_batch_size = 32

        # Train model
        print("Model training")
        model.fit(
            x_train,
            y_train,
            batch_size=num_batch_size,
            epochs=num_epochs,
            validation_data=(x_test, y_test),
            verbose=1,
        )

        # Evaluate model
        print("Model evaluation")
        y_pred_test = model.predict(x_test)
        signature = infer_signature(x_test, y_pred_test)
        print(y_pred_test)
        print(y_pred_test.shape)
        print(y_test.shape)
        test_accuracy = accuracy_score(y_test, (y_pred_test > 0.5).astype("int32"))
        train_accuracy = accuracy_score(
            y_train, (model.predict(x_train) > 0.5).astype("int32")
        )
        print("Test accuracy of the model:", test_accuracy)
        print("Train accuracy of the model:", train_accuracy)

        # Calculate F1 score
        y_pred_test_classes = (y_pred_test > 0.5).astype(
            "int32"
        )  # Convert probabilities to classes
        f1 = f1_score(y_test, y_pred_test_classes)
        print("F1 score:", f1)

        # Log F1 score to MLflow
        mlflow.log_metric("f1_score", f1)

        print("Logging model to MLflow")

        # Log accuracy score to MLflow
        mlflow.log_metric("accuracy_score", test_accuracy)

        mlflow.tensorflow.log_model(
            model,
            artifact_path="model",
            signature=signature,
            input_example=x_test[0],
            registered_model_name="LSTM",
        )
        print("run ID:", run.info.run_id)


if __name__ == "__main__":
    train()
