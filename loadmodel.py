import pickle
import numpy as np


import joblib

model = joblib.load('best_rf_model.pkl')
X_new = np.array([[1, 2, 3,4,5,6,7]])
probabilities = model.predict_proba(X_new)