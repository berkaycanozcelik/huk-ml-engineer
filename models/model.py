import tensorflow as tf
from pydantic import BaseModel
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, \
    RobertaConfig


class PredictionRequest(BaseModel):
    sentence: str
    sentiment: str


class SentimentModel:
    def __init__(self, model_path: str, weights_path: str, config_path: str):
        # Loading the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Loading model configuration
        self.config = RobertaConfig.from_pretrained(config_path)

        # Loading the pre-trained model with the custom configuration
        self.model = TFAutoModelForSequenceClassification.from_pretrained(model_path, config=self.config)

        # Adding custom weights into Model
        self.model.load_weights(weights_path, by_name=True, skip_mismatch=True)

        # Setting the model to evaluation mode
        self.model.trainable = False

    def predict(self, sentence: str):
        # Tokenize the input sentence
        inputs = self.tokenizer(sentence, return_tensors="tf", padding=True, truncation=True, max_length=512)

        # Perform model inference
        outputs = self.model(inputs)
        logits = outputs.logits
        predicted_class = tf.argmax(logits, axis=1).numpy()[0]

        return predicted_class
