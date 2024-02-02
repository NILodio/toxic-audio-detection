import kaggle
import shutil
import zipfile
import pandas as pd
import sqlite3


def extract_and_move(old_name: str, new_name: str):
    shutil.move(old_name, new_name)
    with zipfile.ZipFile(new_name, 'r') as zip_ref:
        zip_ref.extractall('/data')


if __name__ == "__main__":
    api = kaggle.api.KaggleApi()
    api.authenticate()


    api.dataset_download_file('kaggle-username/dataset-name', 'file.zip')
    extract_and_move('file.zip', '/data/dataset-folder')