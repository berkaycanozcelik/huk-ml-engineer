from fastapi import FastAPI, HTTPException
from models.model import SentimentModel, PredictionRequest
import time
import numpy as np

app = FastAPI()

# Initialize the model once during app startup
model_path = "roberta-base"
weights_path = "./huk-data/weights_final.h5"
config_path = "./huk-data/config/config-roberta-base.json"
vocab_path = "./huk-data/config/vocab-roberta-base.json"
merges_path = "./huk-data/config/merges-roberta-base.txt"
sentiment_model = SentimentModel(
    model_path, weights_path, config_path, vocab_path, merges_path
)

# Define a mapping for sentiment labels to model output
sentiment_map = {"neutral": 0, "positive": 1, "negative": 2}


@app.get("/")
async def root():
    return {"message": "Hello HUK"}


# Refer to LATENCY_IMPROVEMENTS.md for strategies to enhance latency
@app.post("/predict")
async def predict(request: PredictionRequest):
    start_time = time.time()  # Starting time measurement for latency

    try:
        # TODO:
        # Check if sentiment is valid
        if request.sentiment not in sentiment_map:
            raise HTTPException(
                status_code=400,
                detail="Invalid sentiment value. Choose from 'neutral', 'positive', 'negative'.",
            )

        # Used the sentiment model to predict the class and logits
        predicted_class, logits, input_ids = sentiment_model.predict(request.sentence)

        # Extracting the attention scores from logits
        attention_scores = np.exp(logits) / np.sum(
            np.exp(logits), axis=1, keepdims=True
        )  # Softmax

        # Mapped the input IDs back to tokens
        tokens = sentiment_model.tokenizer.convert_ids_to_tokens(input_ids[0])

        # Gathered related words based on the requested sentiment
        target_sentiment_class = sentiment_map[request.sentiment]
        related_words = []

        for token, score in zip(tokens, attention_scores[0]):
            if score >= 0.5 and (
                predicted_class == target_sentiment_class
            ):  # Example threshold
                related_words.append(token)

        latency = time.time() - start_time  # Calculating latency
        return {"related_words": related_words, "latency": latency}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during prediction: {str(e)}"
        )
