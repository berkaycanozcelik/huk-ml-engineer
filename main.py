from fastapi import FastAPI, HTTPException
from models.model import SentimentModel, PredictionRequest
import time


app = FastAPI()

# Initialize the model once during app startup
model_path = 'roberta-base'
weights_path = './huk-data/weights_final.h5'
config_path = './huk-data/config/config-roberta-base.json'
sentiment_model = SentimentModel(model_path, weights_path, config_path)


# Define a mapping for sentiment labels to model output
sentiment_map = {
    "neutral": 0,
    "positive": 1,
    "negative": 2
}


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


# Refer to LATENCY_IMPROVEMENTS.md for strategies to enhance latency
@app.post("/predict")
async def predict(request: PredictionRequest):
    start_time = time.time()  # Starting time measurement for latency

    try:
        # Check if sentiment is valid
        if request.sentiment not in sentiment_map:
            raise HTTPException(status_code=400,
                                detail="Invalid sentiment value. Choose from 'neutral', 'positive', 'negative'.")

        # Use the sentiment model to predict the class
        predicted_class = sentiment_model.predict(request.sentence)

        #TODO
        # Compare the predicted class with the target sentiment
        target_sentiment_class = sentiment_map[request.sentiment]

        if predicted_class == target_sentiment_class:
            #TODO
            related_words = request.sentence.split()
        else:
            related_words = []

        latency = time.time() - start_time  # Calculating latency
        return {"related_words": related_words, "latency": latency}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")