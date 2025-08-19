import pandas as pd
from sklearn.linear_model import LinearRegression
from pathlib import Path

class WeightLossPredictor:
    def __init__(self):
        """Initialize the weight loss predictor with the trained model."""
        # Get the directory of the current file
        model_dir = Path(__file__).parent
        data_path = model_dir / "fitness.csv"
        
        # Load and prepare the data
        self.data = pd.read_csv(data_path)
        self.model = self._train_model()
    
    def _train_model(self):
        """Train the linear regression model."""
        x = self.data[[
            "initial_weight", 
            "exercise_minutes", 
            "calories", 
            "water", 
            "sleep_hours", 
            "cheat_days"
        ]]
        
        y = self.data["weight_loss"]
        
        model = LinearRegression()
        model.fit(x, y)
        return model
    
    def predict_weight_loss(self, input_data):
        """
        Predict weight loss based on input parameters.
        
        Args:
            input_data (dict): Dictionary containing input features
                - initial_weight (float): Current weight in kg
                - exercise_minutes (float): Daily exercise in minutes
                - calories (float): Daily calorie intake
                - water (float): Daily water intake in liters
                - sleep_hours (float): Daily sleep hours
                - cheat_days (int): Number of cheat days in 30 days
                
        Returns:
            tuple: (predicted_weight_loss, months_needed)
        """
        # Convert input data to DataFrame for prediction
        input_df = pd.DataFrame([[
            input_data['initial_weight'],
            input_data['exercise_minutes'],
            input_data['calories'],
            input_data['water'],
            input_data['sleep_hours'],
            input_data['cheat_days']
        ]], columns=[
            'initial_weight', 'exercise_minutes', 'calories', 
            'water', 'sleep_hours', 'cheat_days'
        ])
        
        # Make prediction
        predicted_loss = self.model.predict(input_df)[0]
        
        # Calculate months needed to reach goal weight if goal is provided
        months_needed = None
        if 'goal_weight' in input_data and input_data['goal_weight'] > 0:
            total_loss_needed = input_data['initial_weight'] - input_data['goal_weight']
            if total_loss_needed > 0:
                months_needed = total_loss_needed / predicted_loss if predicted_loss > 0 else None
        
        return predicted_loss, months_needed

# Create a singleton instance
weight_loss_predictor = WeightLossPredictor()
