import dill
import json
import pandas as pd
import os
import numpy as np
from datetime import datetime


def predict():
    def get_latest_model_file(directory):
        files = [f for f in os.listdir(directory) if f.endswith('.pkl')]
        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))

        return os.path.join(directory, latest_file)


    path = os.environ.get('my_project_path', '.')
    model_directory = os.path.join(path, 'data', 'models')
    model_path = get_latest_model_file(model_directory)


    with open(model_path, 'rb') as file:
        model = dill.load(file)

    print("Тип модели:", type(model))

    test_data_path = '../data/test'

    predictions = []

    for filename in os.listdir(test_data_path):
        if filename.endswith('.json'):
            file_path = os.path.join(test_data_path, filename)
            with open(file_path, 'r') as fin:
                form = json.load(fin)
                df = pd.DataFrame.from_dict([form])


                y = model.predict(df)
                predictions.append({'id': form['id'], 'prediction': y[0]})
                print(f'{form["id"]}: {y[0]}')

    predictions_df = pd.DataFrame(predictions)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    predictions_path = f'../data/predictions/predictions_{current_time}.csv'

    os.makedirs(os.path.dirname(predictions_path), exist_ok=True)

    predictions_df.to_csv(predictions_path, index=False)
    print(f'Предикт сохранен в  {predictions_path}')


if __name__ == '__main__':
    predict()