# Example file src/datasets.py
import torch
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.X.input_ids)

    def __getitem__(self, index):
        return {
            "input_ids": self.x.input_ids[index],
            "attention_mask": self.x.attention_mask[index],
            "labels": torch.LongTensor([self.y[index]]),
        }


def prepare_dataset(tokenizer, x_raw, y, truncation_length):
    # Tokenize text
    x_preprocessed = tokenizer(
        x_raw.tolist(),
        max_length=truncation_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    dataset = CustomDataset(x_preprocessed, y)  # noqa
