import os

from dotenv import load_dotenv


class CredentialsManager:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        self.load_credentials()

    def load_credentials(self):
        load_dotenv(dotenv_path=self.env_path)

        # Retrieve the credentials from the environment variables
        self._kaggle_username = os.getenv("KAGGLE_USERNAME")
        self._kaggle_password = os.getenv("KAGGLE_KEY")
        self._dataset_kaggle = os.getenv("DATASET_RAW")
        # Add more credentials as needed

    @property
    def kaggle_username(self):
        return self._kaggle_username

    @property
    def kaggle_password(self):
        return self._kaggle_password

    @property
    def dataset_kaggle(self):
        return self._dataset_kaggle
