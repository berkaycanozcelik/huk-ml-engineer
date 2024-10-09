from fastapi import FastAPI
from pydantic import BaseModel

from sentiment_model import SentimentModel


class InputData(BaseModel):
    text: str


app = FastAPI()


model = SentimentModel("weights_final.h5")


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


@app.post("/predict/")
def get_prediction(data: InputData):
    prediction = model.predict(data.text)
    return {"prediction": prediction}
