import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Load your dataset (update the file path as needed)
data = pd.read_csv("data/final_dataset.csv")

# Convert the target column to numeric, setting invalid parsing as NaN
data['label'] = pd.to_numeric(data['label'], errors='coerce')

# Drop rows where the conversion failed (i.e., where target_numeric is NaN)
data = data.dropna(subset=['label'])

# Cast the target column back to a string for classifcation
data['label'] = data['label'].astype(str)

# Separate features and target
X = data.iloc[:, 4:]
y = data["label"]

# Split the data into training and testing sets using stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24, stratify=y
)

# Define a dictionary of candidate classifiers
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=24),
    "Random Forest": RandomForestClassifier(random_state=24),
    "Gradient Boosting": GradientBoostingClassifier(random_state=24),
    "Support Vector Classifier": SVC(probability=True, random_state=24),
    "K-Nearest Neighbors": KNeighborsClassifier()
}

# Evaluate each model using 5-fold cross-validation on the training set
cv_results = {}
print("Cross-Validation Accuracy Scores:")
for name, model in models.items():
    # Using accuracy as the scoring metric; you can switch to "f1_weighted" if desired.
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    cv_results[name] = scores.mean()
    print(f"{name}: {scores.mean():.4f}")

# Determine the best model based on cross-validation performance
best_model_name = max(cv_results, key=cv_results.get)
best_model = models[best_model_name]
print(f"\nBest model based on cross-validation: {best_model_name}")

# Train the best model on the entire training set
best_model.fit(X_train, y_train)

# Make predictions on the test set
predictions = best_model.predict(X_test)

# Evaluate performance on the test set
test_accuracy = accuracy_score(y_test, predictions)
test_f1 = f1_score(y_test, predictions, average="weighted")
print(f"\nTest Accuracy: {test_accuracy:.4f}")
print(f"Test F1 Score: {test_f1:.4f}")