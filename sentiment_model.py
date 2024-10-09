import tensorflow as tf


class SentimentModel:
    def __init__(self, weights_path: str):
        self.model = self.load_model(weights_path)

    def load_model(self, weights_path: str):
        model = tf.keras.models.load_model(weights_path)
        return model

    def predict(self, input_text: str):
        prediction = self.model.predict(input_text)
        return prediction