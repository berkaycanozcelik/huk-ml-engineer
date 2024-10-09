from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf


class InputData(BaseModel):
    text: str


app = FastAPI()


class SentimentModel:
    def __init__(self, weights_path: str):
        self.model = self.load_model(weights_path)

    def load_model(self, weights_path: str):
        model = tf.keras.models.load_model(weights_path)
        return model

    def predict(self, input_text: str):
        prediction = self.model.predict(input_text)
        return prediction


model = SentimentModel("weights_final.h5")


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


@app.post("/predict/")
def get_prediction(data: InputData):
    prediction = model.predict(data.text)
    return {"prediction": prediction}
