import pandas as pd
from sklearn.linear_model import LinearRegression

# Load CSV
data = pd.read_csv("data.csv")  # CSV should have Hours_Studied and Marks columns

# Prepare input and output
X = data[["hrs"]]  # Feature (2D)
y = data["marks"]            # Target (1D)



# to train model
model = LinearRegression()
model.fit(X, y)

# Predict value for given hours

hours = float(input("Enter Hours Studied per day: "))
predicted = model.predict([[hours]])
print(f"Predicted Marks for {hours} hours: {predicted[0]:.2f}")
