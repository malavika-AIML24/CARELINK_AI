import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Step 1: Create synthetic data
def create_synthetic_data(n_samples=1000, n_features=20):
    X = np.random.rand(n_samples, n_features)
    y = np.random.randint(0, 2, n_samples)  # Binary target
    return X, y

# Step 2: Train Random Forest Classifier
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model, X_test, y_test

# Step 3: Evaluate performance
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

# Step 4: Save the model
def save_model(model, filename='model.pkl'):
    joblib.dump(model, filename)

# Step 5: Provide demo predictions
def demo_predictions(model, X_new):
    predictions = model.predict(X_new)
    return predictions

if __name__ == "__main__":
    X, y = create_synthetic_data()
    model, X_test, y_test = train_model(X, y)
    evaluate_model(model, X_test, y_test)
    save_model(model)
    
    # Example of making demo predictions
    X_demo = np.random.rand(5, 20)  # Create 5 new random samples
    print("Demo Predictions:", demo_predictions(model, X_demo))
