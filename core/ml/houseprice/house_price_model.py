# train_house_price_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression

# Step 1: Load a sample dataset
# You can replace this with pd.read_csv('your_data.csv') if using a file
data = pd.DataFrame({
    'Area': [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750],
    'Price': [1500000, 2250000, 3000000, 3750000, 4500000, 5250000, 6000000, 6750000, 7500000, 8250000]
})

# Step 2: Prepare input features (X) and target (y)
X = data[['Area']]  # Feature (area in sq ft)
y = data['Price']   # Target (price in ₹)

# Step 3: Train a Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Step 4: Print the model's learned parameters
print(f"Coefficient (Price per sq ft): ₹{model.coef_[0]:.2f}")
print(f"Intercept (Base price): ₹{model.intercept_:.2f}")

import joblib
joblib.dump(model, 'house_price_model.pkl')