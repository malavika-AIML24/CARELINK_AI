import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class MlRiskPrediction:
    def __init__(self, data):
        self.data = data
        self.model = RandomForestClassifier()

    def preprocess_data(self):
        # Example preprocessing steps
        self.data = self.data.dropna()  # Remove rows with NaN values
        X = self.data.drop('risk_label', axis=1)  # Features
        y = self.data['risk_label']  # Target
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print(classification_report(y_test, y_pred))

    def predict(self, new_data):
        return self.model.predict(new_data)

# Example usage:
# df = pd.read_csv('path_to_data.csv')
# predictor = MlRiskPrediction(df)
# predictor.train_model()