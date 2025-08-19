import joblib
import math
from pathlib import Path

# Get the directory of the current file
MODEL_DIR = Path(__file__).parent
MODEL_PATH = MODEL_DIR / "salary_predictor.pkl"

class SalaryPredictor:
    def __init__(self):
        """Initialize the salary predictor with the trained model."""
        self.model = joblib.load(MODEL_PATH)
    
    def predict_salary(self, years_experience):
        """
        Predict salary based on years of experience.
        
        Args:
            years_experience (int): Years of experience
            
        Returns:
            float: Predicted salary
        """
        return math.ceil(self.model.predict([[years_experience]])[0])

# Create a singleton instance
salary_predictor = SalaryPredictor()
