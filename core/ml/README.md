# 🤖 Machine Learning Models

This directory contains various machine learning models integrated into the Automation Suite. Each model is designed to solve specific prediction and analysis tasks, and can be accessed through the dashboard's ML Models section.

## 📂 Directory Structure

```
core/ml/
├── houseprice/           # House Price Prediction Model
│   ├── app.py           # Streamlit UI for the model
│   ├── model.py         # Model implementation
│   ├── requirements.txt # Dependencies
│   └── README.md        # Model-specific documentation
│
├── marks_predict/       # Student Marks Prediction
│   ├── app.py           # Streamlit UI for the model
│   ├── model.py         # Model implementation
│   ├── data.csv         # Training data
│   └── README.md        # Model-specific documentation
│
├── sal_predictor/       # Salary Prediction
│   ├── app.py           # Streamlit UI for the model
│   ├── model.py         # Model implementation
│   ├── requirements.txt # Dependencies
│   └── README.md        # Model-specific documentation
│
└── weight_loss_estimator/ # Weight Loss Estimation
    ├── app.py           # Streamlit UI for the model
    ├── model.py         # Model implementation
    ├── fitness.csv      # Training data
    └── README.md        # Model-specific documentation
```

## 🏠 House Price Prediction

Predicts house prices based on various features like area, number of bedrooms, location, etc.

**Key Features:**
- Multiple regression model
- Handles both numerical and categorical features
- Interactive visualization of predictions

## 📊 Student Marks Prediction

Predicts student marks based on study hours and other academic factors.

**Key Features:**
- Linear regression model
- Performance visualization
- Study time recommendations

## 💰 Salary Prediction

Predicts salary based on experience, education, and other professional factors.

**Key Features:**
- Multiple linear regression
- Experience level analysis
- Industry comparison

## ⚖️ Weight Loss Estimator

Estimates potential weight loss based on diet and exercise patterns.

**Key Features:**
- Calorie deficit calculation
- Exercise impact analysis
- Goal setting and tracking

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Streamlit (for web interface)
- Required Python packages (see individual model requirements.txt)

### Installation

1. Navigate to the desired model directory:
   ```bash
   cd core/ml/desired_model
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   If no requirements.txt exists, install the common dependencies:
   ```bash
   pip install streamlit pandas numpy scikit-learn matplotlib
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🧠 Model Training

Each model can be retrained with new data. Refer to the individual model's README for specific training instructions. Generally, the process involves:

1. Prepare your training data in the required format
2. Run the training script:
   ```bash
   python model.py --train
   ```
3. The trained model will be saved for future predictions

## 📊 Model Evaluation

Each model includes evaluation metrics that are displayed when training. These typically include:

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- R² Score
- Model accuracy (for classification tasks)

## 🛠️ Usage in Automation Suite

All models are accessible through the Automation Suite dashboard under the "ML Models" section. Each model provides:

- Interactive input forms
- Real-time predictions
- Visualizations of results
- Option to download predictions

## 📚 Model Documentation

Each model has its own detailed documentation in its respective directory. Please refer to the individual README files for:

- Model architecture and methodology
- Input/output specifications
- Training process and parameters
- Performance metrics
- Usage examples

## 🤝 Contributing

We welcome contributions to improve our models! Here's how you can help:

1. **Improve Model Accuracy**
   - Try different algorithms
   - Add more training data
   - Perform feature engineering

2. **Enhance the UI**
   - Add more visualizations
   - Improve user experience
   - Add more interactive elements

3. **Add New Models**
   - Implement new prediction tasks
   - Add support for different data types
   - Create ensemble models

To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is part of the Automation Suite and follows the same licensing terms.

## 📧 Support

For support, please open an issue in the [Automation Suite repository](https://github.com/yourusername/automation-suite/issues).
