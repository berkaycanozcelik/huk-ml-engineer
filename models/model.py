import tensorflow as tf
from pydantic import BaseModel


class InputData(BaseModel):
    text: str


class SentimentModel:
    def __init__(self, model_path: str, weights_path: str):
        self.model = self.load_model(model_path, weights_path)

    def load_model(self, model_path: str, weights_path: str):
        model = tf.keras.models.load_model(model_path)
        model.load_weights(weights_path)
        return model

    def predict(self, input_text: str):
        prediction = self.model.predict(input_text)
        return prediction
