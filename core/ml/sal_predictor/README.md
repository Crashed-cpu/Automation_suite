# Salary Predictor Model

This module implements a machine learning model to predict salary based on years of experience.

## Files

- `__init__.py`: Makes the module importable and creates a singleton instance of the predictor
- `model.py`: Contains the `SalaryPredictor` class with model logic
- `requirements.txt`: Lists the required Python packages
- `*.pkl`: Cached model file (generated automatically)
- `__pycache__/`: Directory containing compiled Python bytecode (generated automatically)

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

## Usage

```python
from core.ml.sal_predictor.model import SalaryPredictor

# Create predictor instance
predictor = SalaryPredictor()

# Predict salary for 5 years of experience
salary = predictor.predict_salary(5)
print(f"Predicted salary: ₹{salary:,.2f}")
```

## Cache Handling

- The trained model is automatically cached to `salary_predictor.pkl` after the first training
- Subsequent imports will load the model from cache for faster startup
- Delete the `.pkl` file to force retraining

## Model Details

- **Algorithm**: Linear Regression
- **Input**: Years of experience (float)
- **Output**: Predicted salary in INR (float)

## Notes

- The model is trained on sample data and should be retrained with real-world data for production use
- Cache files (`.pkl` and `__pycache__`) should not be committed to version control (they are in .gitignore)
