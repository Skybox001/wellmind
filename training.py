import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the data
df = pd.read_excel('Cleaned Data.xlsx')

# Replace Yes and No's with 0s and 1s, and fill NaNs with 0
df.replace({'No': 0, 'Yes': 1}, inplace=True)
df.fillna(0, inplace=True)

# Renaming income columns
age_mapping = {'> 60': 65, '45-60': 52, '30-44': 37, '18-29': 23}
df['Age'] = df['Age'].map(age_mapping)

# Prepare the data
X = df.drop(columns=['Mentaly_ill'])  # Include all features except the target
y = df['Mentaly_ill']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVM model
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluate the model
y_pred = svm_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model to a .pkl file
joblib.dump(svm_model, 'svm_model.pkl')
