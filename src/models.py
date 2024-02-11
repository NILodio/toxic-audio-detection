# Example File
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F  # noqa
from sklearn.metrics import balanced_accuracy_score, f1_score
from transformers import (
    EarlyStoppingCallback,
    IntervalStrategy,
    Trainer,
    TrainingArguments,
)


class Classifier(nn.Module):
    def __init__(self, embedding_tokenizer, embedding_model):
        super().__init__()
        self.embedding_size = 768

        self.embedding = embedding_model
        self.classifier = nn.Linear(self.embedding_size, 1)
        self.sigmoid = torch.sigmoid

    def forward(self, x):
        tokenized = self.tokenizer(
            x,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        outputs = self.embedding(
            input_ids=tokenized.input_ids.cuda(),
            token_type_ids=tokenized.token_type_ids.cuda(),
            attention_mask=tokenized.attention_mask.cuda(),
        )
        pooler_output = outputs.pooler_output
        y = self.classifier(pooler_output)
        return self.sigmoid(y)

    def predict(self, x):
        y = self.forward(x)
        return (y > 0.5).float()


class CustomTrainer(Trainer):
    def __init__(self, class_weights, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = torch.FloatTensor(class_weights).cuda()

    def compute_loss(self, model, inputs, return_outputs=False):  # noqa
        labels = inputs.get("labels").view(-1)

        # forward pass
        outputs = model(**inputs)
        logits = outputs.get("logits")

        # compute custom loss
        loss = F.cross_entropy(logits, labels, weight=self.class_weights)

        return (loss, outputs) if return_outputs else loss


def compute_metrics(p):
    pred, labels = p
    pred = np.argmax(pred, axis=1)
    return {
        "balanced_accuracy": balanced_accuracy_score(y_true=labels, y_pred=pred),
        "f1": f1_score(y_true=labels, y_pred=pred, average="macro"),
    }


def trainer(model, train_dataset, val_dataset, class_weights):
    training_args = TrainingArguments(
        logging_steps=100,
        output_dir="./results",  # output directory
        num_train_epochs=3,  # total # of training epochs
        per_device_train_batch_size=32,  # batch size per device during training
        per_device_eval_batch_size=64,  # batch size for evaluation
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
        weight_decay=0.01,  # strength of weight decay
        logging_dir="./logs",  # directory for storing logs
        evaluation_strategy=IntervalStrategy.STEPS,
        metric_for_best_model="f1",
        load_best_model_at_end=True,
    )
    trainer = CustomTrainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=train_dataset,  # training dataset
        eval_dataset=val_dataset,  # evaluation dataset
        class_weights=class_weights,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    trainer.train()
