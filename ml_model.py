import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

FEATURES = ["similarity", "matched", "missing", "percent", "length"]

def train_model():
    print("Loading training data...")
    data = pd.read_csv("universal_training_data_200.csv")

    X = data[FEATURES]
    y = data["label"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Accuracy
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Save model
    pickle.dump(model, open("model.pkl", "wb"))
    print("Saved successfully as model.pkl!")

def predict(features):
    model = pickle.load(open("model.pkl", "rb"))

    # features should be in same order
    features_df = pd.DataFrame([features], columns=FEATURES)

    result = model.predict(features_df)
    return result[0]

if __name__ == "__main__":
    train_model()