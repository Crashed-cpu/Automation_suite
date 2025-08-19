import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

class MarksPredictor:
    def __init__(self):
        self.model = None
        self.data_path = os.path.join(os.path.dirname(__file__), 'data.csv')
        self.model_path = os.path.join(os.path.dirname(__file__), 'marks_predictor.pkl')
        self.load_model()
    
    def load_model(self):
        """Load the model from disk or train a new one if not found."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the model using the data from data.csv."""
        try:
            # Load data
            data = pd.read_csv(self.data_path)
            
            # Prepare input and output
            X = data[["hrs"]]  # Feature (2D)
            y = data["marks"]  # Target (1D)
            
            # Train model
            self.model = LinearRegression()
            self.model.fit(X, y)
            
            # Save the trained model
            joblib.dump(self.model, self.model_path)
            
        except Exception as e:
            raise Exception(f"Error training the model: {str(e)}")
    
    def predict_marks(self, hours_studied):
        """
        Predict marks based on hours studied.
        
        Args:
            hours_studied (float): Number of hours studied per day
            
        Returns:
            float: Predicted marks (0-100)
        """
        if self.model is None:
            self.train_model()
        
        try:
            # Ensure input is a float
            hours = float(hours_studied)
            
            # Predict and ensure marks are within 0-100 range
            predicted = self.model.predict([[hours]])
            predicted_marks = max(0, min(100, predicted[0]))  # Clamp between 0 and 100
            
            # Calculate study recommendation
            recommendation = self._get_study_recommendation(hours, predicted_marks)
            
            return round(predicted_marks, 2), recommendation
            
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")
    
    def _get_study_recommendation(self, hours_studied, predicted_marks):
        """Generate a study recommendation based on hours and predicted marks."""
        if predicted_marks < 40:
            return ("⚠️ Your study time might need improvement. Consider increasing your study hours "
                   "and focusing on active learning techniques.")
        elif predicted_marks < 70:
            return ("👍 Good effort! You're on the right track. Consider adding 1-2 more hours "
                   "of focused study to improve your marks further.")
        elif predicted_marks < 90:
            return ("🎉 Excellent work! You're doing great. Maintain this study routine for consistent results.")
        else:
            return ("🏆 Outstanding performance! You've mastered effective study techniques. "
                   "Consider helping your peers or exploring advanced topics.")
