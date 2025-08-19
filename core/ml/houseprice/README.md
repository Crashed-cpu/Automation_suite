# House Price Predictor

This module provides a machine learning model to estimate house prices based on property area and location type.

## Files

- `__init__.py`: Makes the module importable and creates a singleton instance of the predictor
- `model.py`: Contains the `HousePricePredictor` class with model logic
- `house_price_model.py`: Original model training script
- `house_price_model.pkl`: Serialized trained model (generated automatically)
- `requirements.txt`: Lists the required Python packages
- `__pycache__/`: Directory containing compiled Python bytecode (generated automatically)

## Requirements

Install the required packages using:
```bash
pip install -r requirements.txt
```

## Usage

```python
from core.ml.houseprice.model import HousePricePredictor

# Create predictor instance
predictor = HousePricePredictor()

# Predict price for a 1500 sq ft property in an urban area
price, price_per_sqft, multiplier = predictor.predict_price(1500, "urban")
print(f"Predicted price: ₹{price:,.2f}")
print(f"Price per sq ft: ₹{price_per_sqft:,.2f}")
print(f"Location multiplier: {multiplier}x")
```

## Cache Handling

- The trained model is automatically cached to `house_price_model.pkl` after the first training
- Subsequent imports will load the model from cache for faster startup
- Delete the `.pkl` file to force retraining
- The `__pycache__` directory contains compiled Python bytecode for faster imports

## Model Details

- **Algorithm**: Linear Regression with location-based multipliers
- **Input**:
  - Area (square feet)
  - Location type ('urban', 'suburban', or 'rural')
- **Output**:
  - Predicted price (float)
  - Price per square foot (float)
  - Location multiplier (float)

## Location Multipliers

- **Urban**: 1.2x base price
- **Suburban**: 1.0x base price
- **Rural**: 0.8x base price

## Notes

- The model is trained on sample data and should be retrained with real-world data for production use
- Cache files (`.pkl` and `__pycache__`) are automatically generated and should not be committed to version control
- The model provides rough estimates and should be used as a starting point for price evaluation
