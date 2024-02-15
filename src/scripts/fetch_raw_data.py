import os

import kaggle
from prefect import flow, task

from config.credentials import CredentialsManager


@task()
def dowload_data(df: str, usr_name: str, key: str):
    k = kaggle.KaggleApi({"username": usr_name, "key": key})
    k.authenticate()
    print("✅ Kaggle: user authenticated")
    print("\tDownloading Data")
    # check current directory
    print(f"Current directory: {os.getcwd()}")
    print("print root directory" + os.path.abspath("datasets"))
    print("✅ Kaggle: dataset downloaded")
    print("✅ Kaggle: data ready")
    # print the files in the directory


@flow(log_prints=True)
def data():
    print("Fetching data")
    credentials = CredentialsManager()
    dowload_data(
        df=credentials.dataset_kaggle,
        usr_name=credentials.kaggle_username,
        key=credentials.kaggle_password,
    )


if __name__ == "__main__":
    data()
