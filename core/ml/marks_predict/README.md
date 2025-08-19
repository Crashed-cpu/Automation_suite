# Marks Predictor

This module implements a machine learning model to predict academic marks based on study hours.

## Files

- `__init__.py`: Makes the module importable and creates a singleton instance of the predictor
- `model.py`: Contains the `MarksPredictor` class with model logic
- `data.csv`: Sample dataset used for training the model
- `requirements.txt`: Lists the required Python packages
- `__pycache__/`: Directory containing compiled Python bytecode (generated automatically)

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

## Usage

```python
from core.ml.marks_predict.model import MarksPredictor

# Create predictor instance
predictor = MarksPredictor()

# Predict marks for 3.5 hours of study per day
marks, recommendation = predictor.predict_marks(3.5)
print(f"Predicted marks: {marks:.1f}/100")
print(f"Recommendation: {recommendation}")
```

## Cache Handling

- The trained model is automatically cached to `marks_predictor.pkl` after the first training
- Subsequent imports will load the model from cache for faster startup
- Delete the `.pkl` file to force retraining
- The `__pycache__` directory contains compiled Python bytecode for faster imports

## Model Details

- **Algorithm**: Linear Regression
- **Input**: Study hours per day (float)
- **Output**:
  - Predicted marks (0-100)
  - Study recommendation (string)

## Data Format

The model is trained on a CSV file with the following columns:
- `name`: Student name (not used in training)
- `hrs`: Study hours per day
- `marks`: Obtained marks (0-100)

## Notes

- The model provides estimates based on the training data
- For best results, retrain the model with your own dataset
- Cache files (`.pkl` and `__pycache__`) are automatically generated and should not be committed to version control
