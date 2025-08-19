# Weight Loss Estimator

This module provides a machine learning model to estimate weight loss based on various lifestyle factors.

## Files

- `__init__.py`: Makes the module importable and creates a singleton instance of the predictor
- `model.py`: Contains the `WeightLossPredictor` class with model logic
- `fitness.csv`: Sample dataset used for training the model
- `requirements.txt`: Lists the required Python packages
- `__pycache__/`: Directory containing compiled Python bytecode (generated automatically)

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

## Usage

```python
from core.ml.weight_loss_estimator.model import WeightLossPredictor

# Create predictor instance
predictor = WeightLossPredictor()

# Prepare input data
input_data = {
    'initial_weight': 70.0,     # kg
    'goal_weight': 65.0,        # kg
    'exercise_minutes': 30,     # minutes/day
    'calories': 2000,           # kcal/day
    'water': 2.5,               # liters/day
    'sleep_hours': 7.5,         # hours/night
    'cheat_days': 2             # days/month
}

# Get prediction
weight_loss, months_needed = predictor.predict_weight_loss(input_data)
print(f"Estimated weight loss: {weight_loss:.2f} kg in 30 days")
print(f"Time to reach goal: {months_needed:.1f} months")
```

## Cache Handling

- The trained model is automatically cached after the first training
- Model weights are stored in memory after first use for faster predictions
- The module handles model loading and caching automatically

## Model Details

- **Algorithm**: Linear Regression with multiple features
- **Input**:
  - Initial weight (kg)
  - Goal weight (kg)
  - Daily exercise (minutes)
  - Daily calorie intake (kcal)
  - Daily water intake (liters)
  - Sleep hours per night
  - Cheat days per month
- **Output**:
  - Predicted weight loss in 30 days (kg)
  - Estimated months to reach goal weight

## Notes

- The model provides estimates based on general patterns and may not be accurate for all individuals
- For best results, input accurate and honest measurements
- Consult with a healthcare professional for personalized advice
