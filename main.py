from fastapi import FastAPI
from models.model import SentimentModel, InputData
import time

app = FastAPI()

model = SentimentModel("huk-data/model.h5", "huk-data/weights_final.h5")


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


# Refer to LATENCY_IMPROVEMENTS.md for strategies to enhance latency
@app.post("/predict/", response_model=dict)
def get_prediction(data: InputData) -> dict:
    """
    Predict sentiment from input text.

    Args:
        data (InputData): Input data containing the text to analyze.

    Returns:
        dict: A dictionary containing the prediction result.
    """
    start_time = time.time()
    prediction = model.predict(data.text)
    latency = time.time() - start_time
    return {"prediction": prediction, "latency": latency}
