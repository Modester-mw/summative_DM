import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow import keras

def preprocess_data(course, status, current_courses, topics, scores, time_spent):
    # Create a DataFrame with the input data
    df = pd.DataFrame({
            'course': [course],
            'status': [status],
            'current_courses': [current_courses],
            'topics': [topics],
            'scores': [scores],
            'time_spent': [time_spent]
        })

    # Replace missing values with default values
    new_df = df.fillna({
            'status': 'Not started',
            'current_courses': '',
            'topics': '',
            'scores': 0,
            'time_spent': 0
        })

    # One-hot encode categorical features
    course_encoded = pd.get_dummies(df['course'], prefix='course')
    status_encoded = pd.get_dummies(df['status'], prefix='status')
    new_df = pd.concat([new_df, course_encoded, status_encoded], axis=1)
    new_df = new_df.drop(['course', 'status'], axis=1)

    # Scale numerical features
    numeric_features = ['scores', 'time_spent']
    new_df[numeric_features] = new_df[numeric_features].apply(lambda x: (x - np.mean(x)) / np.std(x))

    return new_df

def build_model(input_shape):
    # Define the model architecture
    model = Sequential()
    model.add(Dense(64, input_shape=input_shape, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    print()

    return model

def train_model(new_df):
    # Split the data into input and output variables
    X = new_df.drop('target', axis=1)
    y = new_df['target']

    # Build the model
    model = build_model((X.shape[1],))

    # Train the model
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

    # Save the trained model
    model.save('/Users/foundation/Desktop/prediction_user/model/trained_model.h5')
    print("model_saved")

def predict(course, status, current_courses, topics, scores, time_spent):
    # Load the trained model
    model = keras.models.load_model('/Users/foundation/Desktop/prediction_user/model/trained_model.h5')

    # Preprocess the input data
    input_data = preprocess_data(course, status, current_courses, topics, scores, time_spent)

    # Make predictions on the input data
    prediction = model.predict(input_data)[0]

    # Convert the prediction to a human-readable format
    if prediction >= 0.5:
        return 'Likely to complete the course'
    else:
        return 'Likely to drop out of the course'

# Example usage

prediction = predict('Mathematics', 'In progress', 'Science, Literature', 'Algebra', 80, 5)
print(prediction)
