import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import *
from sklearn.preprocessing import StandardScaler

# Load data function
def load_data(file):
    df = pd.read_csv(file)
    return df

#new
# Data preprocessing function
def preprocess_data(df):
    # Annahme: Auswertung von Lernaufgaben basiert auf der durchschnittlichen Bewertung der Aufgaben
    df['Auswertung_Lernaufgaben'] = df[['Abgabe1', 'Abgabe2', 'Abgabe3']].mean(axis=1)

    # Annahme: Lernaktivitäten basieren auf der Summe verschiedener Aktivitäten
    df['Lernaktivitaeten'] = df[['Anz_Zugriffe', 'Anz_Forum', 'Anz_Post', 'Anz_Quiz_Pruefung']].sum(axis=1)

    return df

# Train model function
def train_model(X_train_scaled, y_train):
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    return model

# Main function
def main():
    st.title("Lernfortschritt Analysis")

    # File upload
    #uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    uploaded_file = 1

    if uploaded_file is not None:
        # Load and preprocess data
        #df = load_data(uploaded_file)
        df = load_data('Student_Performance.csv')
        df = preprocess_data(df)

        # Display the raw data
        st.subheader("Raw Data")
        st.write(df)

        # Feature selection
        st.header("Feature Selection")
        features = st.multiselect("Select Features", df.columns)

        # Split data and train model
        target = 'Abschlussnote'
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        # Train the model
        model = train_model(X_train_scaled, y_train)

        # Overall Results
        st.subheader("Overall Results")
        y_pred_test = model.predict(scaler.transform(X_test))
        mae_test = mean_absolute_error(y_test, y_pred_test)  # Use mean_absolute_error
        st.write(f'Mean Absolute Error (Linear Regression): {mae_test}')

        # Filter for Each Student
        st.header("Filter for Each Student")
        student_list = df['Student_ID'].unique()
        selected_student = st.selectbox("Select a Student ID", student_list)

        # Filter data for the selected student
        filtered_data = df[df['Student_ID'] == selected_student]
        
        # Predictions for the selected student
        X_selected = filtered_data[features]
        y_selected_pred = model.predict(scaler.transform(X_selected))

        # Display predictions
        st.subheader("Predicted performance for each student")
        st.write(f'Predicted Abschlussnote for {selected_student}: {y_selected_pred}')

if __name__ == "__main__":
    main()

