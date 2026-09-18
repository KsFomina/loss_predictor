import json
import joblib
import pandas as pd

class ModelWrapper:
    def __init__(self, model_path:str, metadata_path:str):
        self.model=joblib.load(model_path)
        with open(metadata_path, "r") as f:
            self.metadata=json.load(f)

        self.version:str =self.metadata["model_version"]
        self.feature_columns: list[str] =self.metadata["features"]
    
    def predict(self, features:dict)-> float:
        df=pd.DataFrame([features])
        df=df[self.feature_columns] #требуемый порядок
        result=self.model.predict(df)

        return float(result[0])

'''
from config import MODEL_PATH, MODEL_METADATA_PATH

m = ModelWrapper(MODEL_PATH, MODEL_METADATA_PATH)
print("version:", m.version)
print("features:", m.feature_columns)

features = {
    "item_price": 2500.0,
    "delivery_days": 4,
    "client_is_app": True,
    "type_prepayment": "card",
    "historical_return_rate": 0.773956,
    "avg_item_losses_30d": 623.1971,
}

pred = m.predict(features)
print("prediction:", pred)
print("rounded:", round(pred, 2))
'''