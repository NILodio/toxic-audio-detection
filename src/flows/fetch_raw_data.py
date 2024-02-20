import os

import kaggle
from prefect import flow, task
from prefect.filesystems import RemoteFileSystem

from core.credentials import CredentialsManager

remote_file_system_block = RemoteFileSystem.load("data")


@task()
def dowload_data(df: str, usr_name: str, key: str):
    k = kaggle.KaggleApi({"username": usr_name, "key": key})
    k.authenticate()
    print("✅ Kaggle: user authenticated")
    print("\tDownloading Data")
    print(f"\tDataset: {df}")
    print(os.getcwd())
    k.dataset_download_cli(df, unzip=True, force=True, path="../data/raw")

    remote_file_system_block.put("data/raw", "data/raw")


@flow(log_prints=True, persist_result=True, result_storage=remote_file_system_block)
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
