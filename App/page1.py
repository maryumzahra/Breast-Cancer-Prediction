import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import re
from chatbot_database import CHATBOT_RESPONSES, POSSIBLE_QUESTIONS, USER_GUIDE_TEXT, get_response  

# Function to clean the data
def clean_data():
    data = pd.read_csv(r'C:\\Users\\Natasha\\Breast-Cancer-Prediction\\Data\\data.csv')
    # Drop unnecessary columns
    data = data.drop(['Unnamed: 32', 'id'], axis=1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data

# Sidebar for user inputs
def sidebar():
    st.sidebar.header("Cell Nuclei Measurements")

    data = clean_data()

    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}  # This dictionary will be used to create charts 

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(label,
                                           min_value=float(0), 
                                           max_value=float(data[key].max()), 
                                           value=float(data[key].mean())
                                          )
    
    return input_dict

# Dynamic donut chart for predictions
def dynamic_donut_chart(input_data):
    model = pickle.load(open(r'C:\\Users\\Natasha\\Breast-Cancer-Prediction\\Model\\model.pkl', 'rb'))
    scaler = pickle.load(open(r'C:\\Users\\Natasha\\Breast-Cancer-Prediction\\Model\\scaler.pkl', 'rb'))

    # Prepare the input data
    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    # Get probabilities from the model
    probabilities = model.predict_proba(input_array_scaled)[0]  # [P(Benign), P(Malignant)]
    
    # Prepare data for the chart
    chart_data = pd.DataFrame({
        'Diagnosis': ['Benign', 'Malignant'],
        'Probability': probabilities
    })

    # Create a dynamic donut chart
    fig = px.pie(
        chart_data,
        values='Probability',
        names='Diagnosis',
        hole=0.6,
        color='Diagnosis',
        color_discrete_map={'Benign': 'green', 'Malignant': 'red'}
    )

    fig.update_layout(
        annotations=[dict(
            text=f"{int(probabilities[1] * 100):.0f}% Malignant",
            showarrow=False,
            font=dict(size=12)
        )],
        autosize=False,
        width=400,
        height=400,
        margin=dict(l=20,r=20,b=100,t=100,pad=0),
        showlegend=False

    )

    return fig

# Radar chart to visualize the input data
def chart(input_data):  # Input data is a dictionary
    input_data = scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 
                  'Concavity', 'Concave Points', 'Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
           input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
           input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
           input_data['fractal_dimension_mean']],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'], input_data['area_se'],
           input_data['smoothness_se'], input_data['compactness_se'], input_data['concavity_se'],
           input_data['concave points_se'], input_data['symmetry_se'], input_data['fractal_dimension_se']],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
           input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
           input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
           input_data['fractal_dimension_worst']],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        autosize=False,
        width=400,
        height=400,
        margin=dict(l=50,r=50,b=100,t=100, pad=4),
        showlegend=False
    )

    return fig

# Predictions function for the model
def predictions(input_data):
    model = pickle.load(open(r'C:\\Users\\Natasha\\Breast-Cancer-Prediction\\Model\\model.pkl', 'rb'))
    scaler = pickle.load(open(r'C:\\Users\\Natasha\\Breast-Cancer-Prediction\\Model\\scaler.pkl', 'rb'))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    probabilities = model.predict_proba(input_array_scaled)[0]
    prediction = model.predict(input_array_scaled)

    confidence = float(probabilities[prediction]) * 100
    
    if prediction[0] == 0:
        st.write('The tumor is predicted to be **Benign**.')
    else:
        st.write('The tumor is predicted to be **Malignant**.')

    st.write(f'Confidence: {confidence:.2f}%')

# Function to scale the input values
def scaled_values(input_dict):
    data = clean_data()

    X = data.drop(['diagnosis'], axis=1)

    scaled_dict = {}

    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value
    
    return scaled_dict

# Chatbot-related functions (like responses and guide text)
def chatbot():
    # Input for the chatbot query
    query = st.text_input("Ask me anything:")

    # Display the chatbot response if there's a query
    if query:
        st.write(get_response(query))

    # Button to show possible questions
    if st.button("Possible Questions"):
        st.write(POSSIBLE_QUESTIONS)

    # Button to show user guide
    if st.button("User Guide"):
        st.write(USER_GUIDE_TEXT)

# Main function to run the app
def main():
     st.set_page_config(
        page_title= 'Cancer Prediction',
        page_icon= ':female-doctor:',
        layout= 'wide',
        initial_sidebar_state= 'expanded',

        )
     
     input_data = sidebar()
     with st.container():
        st.title('Breast Cancer Predictor')
          # Display Prediction
        st.subheader('Cell cluster Prediction')
        predictions(input_data)
     
     col1, col2, col3 = st.columns([2,2,1])  

    
     with col1: #Radar Chart
        radar_chart= chart(input_data)
        st.plotly_chart(radar_chart)

     with col2:
        # Display Donut Chart for Prediction Probability
        #st.subheader("Prediction Probability")
        st.plotly_chart(dynamic_donut_chart(input_data), use_container_width=True)
        
    
            

     with col3:
    
        #st.write('The results generated by this tool should be interpreted by qualified medical practitioners and should not be considered as a definitive diagnosis.')
        # Chatbot section
        chatbot()
    

    
    ## Remove this========================
    # Display Radar Chart
    #st.subheader("Tumor Characteristics Radar Chart")
    #st.plotly_chart(chart(input_data), use_container_width=True)
    #=====================================

    

    

if __name__ == "__main__":
    main()
