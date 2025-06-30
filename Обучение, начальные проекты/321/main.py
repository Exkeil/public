import dill
import json
import numpy as np
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
with open('Homework_pipe.plk', 'rb') as file:
    model = dill.load(file)


class Form(BaseModel):
    id: int
    url: str
    region: str
    region_url: str
    price: int
    year: float
    manufacturer: str
    model: str
    fuel: str
    odometer: float
    title_status: str
    transmission: str
    image_url: str
    description: str
    state: str
    lat: float
    long: float
    posting_date: str


class Prediction(BaseModel):
    id: str
    price: int
    Result: float


@app.get('/status')
def status():
    return "I'm okay"

@app.get('/version')
def version():
    return model['metadata']

@app.post('/predict', response_model= Prediction)
def predict(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])
    y = model['model'].predict(df)

    return {
        'id': form.id,
        'price': form.price,
        'Result': y[0]
    }


def main():
    with open('homework_pipe.plk', 'rb') as file:
        model = dill.load(file)

    with open('data/7310993818.json') as fin:
        form = json.load(fin)
        df = pd.DataFrame.from_dict([form])
        y = model['model'].predict(df)
        print(f'{form["id"]}: {y[0]}')



