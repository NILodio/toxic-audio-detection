import os

import kaggle

from config.credentials import CredentialsManager


def dowload_data(df: str, usr_name: str, key: str):
    if not os.path.exists("data"):
        os.makedirs("data")
    k = kaggle.KaggleApi({"username": usr_name, "key": key})
    k.authenticate()
    print("kaggle.com: authenticated")
    print(f"Downloading {df} dataset")
    print(f"usr_name {usr_name} key {key}")
    k.dataset_download_cli(dataset=df, unzip=True, path="data")


if __name__ == "__main__":
    credentials = CredentialsManager()
    dowload_data(
        df=credentials.dataset_kaggle,
        usr_name=credentials.kaggle_username,
        key=credentials.kaggle_password,
    )
