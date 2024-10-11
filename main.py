from fastapi import FastAPI
from models.model import SentimentModel, InputData

app = FastAPI()

model = SentimentModel("huk-data/models.h5", "huk-data/weights_final.h5")


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


@app.post("/predict/", response_model=dict)
def get_prediction(data: InputData) -> dict:
    """
    Predict sentiment from input text.

    Args:
        data (InputData): Input data containing the text to analyze.

    Returns:
        dict: A dictionary containing the prediction result.
    """
    prediction = model.predict(data.text)
    return {"prediction": prediction}
