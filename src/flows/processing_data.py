import io

import pandas as pd
from prefect import flow, task
from prefect.filesystems import RemoteFileSystem
from pydub import AudioSegment

remote_file_system_block = RemoteFileSystem.load("data")


@task()
def get_metadata(metadata_path: str) -> pd.DataFrame:
    file_content = remote_file_system_block.read_path(metadata_path)
    buffer = io.BytesIO(file_content)
    metadata = pd.read_excel(buffer, sheet_name="read_dataset")
    return metadata


@task()
def process_metadata(metadata: pd.DataFrame):
    print(metadata.head())


@task()
def violente_audios(
    metadata: pd.DataFrame, violence_path: str = "processed/violence_data/"
):
    for record in metadata.values:
        t1 = 1000 * record[2]
        t2 = 1000 * record[3]
        audio_content = remote_file_system_block.read_path(
            "raw/audios_VSD/audios_VSD/" + str(record[0]) + ".wav"
        )
        audio = AudioSegment.from_wav(io.BytesIO(audio_content))
        violence_segment = audio[t1:t2]
        violence_bytes = violence_segment.export(format="wav").read()
        remote_file_system_block.write_path(
            path=violence_path + str(record[0]) + "_violence.wav",
            content=violence_bytes,
        )


@task()
def no_violente_audios(
    metadata: pd.DataFrame, no_violence_path: str = "processed/no_violence_data/"
):
    for record in metadata.values:
        t1 = 1000 * record[2]
        audio_content = remote_file_system_block.read_path(
            "raw/audios_VSD/audios_VSD/" + str(record[0]) + ".wav"
        )
        audio = AudioSegment.from_wav(io.BytesIO(audio_content))
        no_violence_segment = audio[0:t1]
        no_violence_bytes = no_violence_segment.export(format="wav").read()
        remote_file_system_block.write_path(
            path=no_violence_path + str(record[0]) + "_non_violence.wav",
            content=no_violence_bytes,
        )


@flow(log_prints=True)
def proccesing():
    metadata = get_metadata(metadata_path="/raw/VSD.xlsx")
    print("Processing Violent Audios")
    violente_audios(metadata)
    print("Processing Non-Violent Audios")
    no_violente_audios(metadata)


if __name__ == "__main__":
    proccesing()
