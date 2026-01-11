import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # Ensure numeric types
        X["current_price"] = pd.to_numeric(X["current_price"], errors="coerce")
        X["original_price"] = pd.to_numeric(X["original_price"], errors="coerce")
        X["pages"] = pd.to_numeric(X["pages"], errors="coerce")

        # Feature engineering
        X["discount_rate"] = (
            X["original_price"] - X["current_price"]
        ) / X["original_price"]

        X["price_per_page"] = X["current_price"] / X["pages"]

        # Handle inf values
        X.replace([np.inf, -np.inf], np.nan, inplace=True)

        return X

