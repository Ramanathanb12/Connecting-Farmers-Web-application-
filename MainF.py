#========================== IMPORT PACKAGES ============================

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn import preprocessing
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#=========================== DATA SELECTION ============================

# Load the dataset
dataframe = pd.read_csv("Price_Agriculture_commodities_Week.csv")

# Show the first 15 rows of the dataframe
print("----------------------------------------")
print("     Data Selection                     ")
print("----------------------------------------")
print()
print(dataframe.head(15))

#========================== PRE PROCESSING ================================

#====== CHECKING MISSING VALUES ========
print("----------------------------------------")
print("             Handling Missing values    ")
print("----------------------------------------")
print()
print(dataframe.isnull().sum())

#===== LABEL ENCODING =====
label_encoder = preprocessing.LabelEncoder()

print("-------------------------------------------------------------")
print(" Before label encoding ")
print("-------------------------------------------------------------")
print()
print(dataframe['State'].head(15))

# Apply label encoding to categorical columns
dataframe['State'] = label_encoder.fit_transform(dataframe['State'])
dataframe['District'] = label_encoder.fit_transform(dataframe['District'])
dataframe['Market'] = label_encoder.fit_transform(dataframe['Market'])
dataframe['Commodity'] = label_encoder.fit_transform(dataframe['Commodity'])
dataframe['Variety'] = label_encoder.fit_transform(dataframe['Variety'])
dataframe['Grade'] = label_encoder.fit_transform(dataframe['Grade'])
dataframe['Arrival_Date'] = label_encoder.fit_transform(dataframe['Arrival_Date'])

print("-------------------------------------------------------------")
print(" After label encoding ")
print("-------------------------------------------------------------")
print()
print(dataframe['State'].head(15))

#========================== DATA SPLITTING ===========================

# Split the data into features (X) and target (y)
X = dataframe.drop(['Modal Price'], axis=1)
y = dataframe['Modal Price']


# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

print("----------------------------------------")
print("             Data Splitting              ")
print("----------------------------------------")
print()

print("Total no of input data   :", dataframe.shape[0])
print("Total no of test data    :", X_test.shape[0])
print("Total no of train data   :", X_train.shape[0])

#========================== MODEL TRAINING ===========================

# Initialize the RandomForestRegressor model
rf = RandomForestRegressor()

# Train the model on the training data
rf.fit(X_train, y_train)

#========================== MAKING PREDICTIONS ===========================

# Make predictions using the trained RandomForestRegressor model
pred_rf = rf.predict(X_test)

#========================== EVALUATION METRICS ===========================

# Calculate the Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared (R²)
mae = mean_absolute_error(y_test, pred_rf)
mse = mean_squared_error(y_test, pred_rf)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, pred_rf)

# Print the evaluation metrics
print("----------------------------------------")
print("Random Forest              ")
print("----------------------------------------")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R-squared (R²): {r2}")

accuracy_regression = r2 * 100
print(f"Regression Model 'Accuracy' (R²): {accuracy_regression}")
# ---------------------------------------------------
import joblib

# Save the trained model to a file
model_filename = "random_forest_model.pkl"
joblib.dump(rf, model_filename)
print(f"\nModel saved as '{model_filename}'")


# Load the saved model
loaded_model = joblib.load(model_filename)
print("\nModel loaded successfully!")

# Take user input
print("\nEnter the following details for prediction:")

state = int(input("State (encoded): "))
district = int(input("District (encoded): "))
market = int(input("Market (encoded): "))
commodity = int(input("Commodity (encoded): "))
variety = int(input("Variety (encoded): "))
grade = int(input("Grade (encoded): "))
Arrival_Date = int(input("Arrival_Date (encoded): "))

min_price = float(input("Minimum Price: "))
max_price = float(input("Maximum Price: "))
# arrival_quantity = float(input("Arrival Quantity: "))

# Combine user input into a NumPy array and reshape it
user_data = np.array([[state, district, market, commodity, variety, grade,Arrival_Date,  min_price, max_price]])

# Predict using the loaded model
predicted_modal_price = loaded_model.predict(user_data)
print(f"\nPredicted Modal Price: ₹{predicted_modal_price[0]:.2f}")


