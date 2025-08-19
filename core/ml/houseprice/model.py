import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

class HousePricePredictor:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
        self.load_model()
    
    def load_model(self):
        """Load the model from disk or train a new one if not found."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the model using sample data."""
        try:
            # Sample data (can be replaced with actual data loading)
            data = pd.DataFrame({
                'Area': [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750],
                'Price': [1500000, 2250000, 3000000, 3750000, 4500000, 
                         5250000, 6000000, 6750000, 7500000, 8250000]
            })
            
            # Prepare input and output
            X = data[['Area']]  # Feature (area in sq ft)
            y = data['Price']   # Target (price in ₹)
            
            # Train model
            self.model = LinearRegression()
            self.model.fit(X, y)
            
            # Save the trained model
            joblib.dump(self.model, self.model_path)
            
        except Exception as e:
            raise Exception(f"Error training the model: {str(e)}")
    
    def predict_price(self, area, location_type='urban'):
        """
        Predict house price based on area and location type.
        
        Args:
            area (float): Area of the house in square feet
            location_type (str): Type of location ('urban', 'suburban', 'rural')
            
        Returns:
            tuple: (predicted_price, price_per_sqft, location_multiplier)
        """
        if self.model is None:
            self.train_model()
        
        try:
            # Ensure input is a float
            area = float(area)
            
            # Apply location multiplier (example values)
            location_multipliers = {
                'urban': 1.2,
                'suburban': 1.0,
                'rural': 0.8
            }
            
            # Get base prediction
            base_price = self.model.predict([[area]])[0]
            
            # Apply location multiplier
            multiplier = location_multipliers.get(location_type.lower(), 1.0)
            predicted_price = base_price * multiplier
            
            # Calculate price per sqft
            price_per_sqft = predicted_price / area if area > 0 else 0
            
            return (
                max(0, predicted_price),  # Ensure non-negative price
                price_per_sqft,
                multiplier
            )
            
        except Exception as e:
            raise Exception(f"Error making prediction: {str(e)}")
    
    def get_model_parameters(self):
        """Get the model's learned parameters."""
        if self.model is None:
            self.train_model()
            
        return {
            'coefficient': self.model.coef_[0] if hasattr(self.model, 'coef_') else 0,
            'intercept': self.model.intercept_ if hasattr(self.model, 'intercept_') else 0
        }
