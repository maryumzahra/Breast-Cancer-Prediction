import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def clean_data():
    data= pd.read_csv('data/data.csv')
    
    # Drop unnecessary columns
    data = data.drop(['Unnamed: 32', 'id'], axis = 1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    
    return data

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

    input_dict = {} #This dictionary will be used to create charts 

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider( label,
        min_value= float(0), 
        max_value= float(data[key].max()), 
        value= float(data[key].mean())
        ) 
    
    return input_dict

def chart(input_data): # Input data is a dictionary

    input_data = scaled_values(input_data)
    categories = ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness', 'Compactness', 
                'Concavity', 'Concave Points','Symmetry', 'Fractal Dimension']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
    r=[
          input_data['radius_mean'], input_data['texture_mean'], input_data['perimeter_mean'],
          input_data['area_mean'], input_data['smoothness_mean'], input_data['compactness_mean'],
          input_data['concavity_mean'], input_data['concave points_mean'], input_data['symmetry_mean'],
          input_data['fractal_dimension_mean']
        ],
        theta=categories,
        fill='toself',
        name='Mean Value'
    ))


    fig.add_trace(go.Scatterpolar(
        r=[
          input_data['radius_se'], input_data['texture_se'], input_data['perimeter_se'], input_data['area_se'],
          input_data['smoothness_se'], input_data['compactness_se'], input_data['concavity_se'],
          input_data['concave points_se'], input_data['symmetry_se'],input_data['fractal_dimension_se']
        ],
        theta=categories,
        fill='toself',
        name='Standard Error'
    ))

    
    fig.add_trace(go.Scatterpolar(
         r=[
          input_data['radius_worst'], input_data['texture_worst'], input_data['perimeter_worst'],
          input_data['area_worst'], input_data['smoothness_worst'], input_data['compactness_worst'],
          input_data['concavity_worst'], input_data['concave points_worst'], input_data['symmetry_worst'],
          input_data['fractal_dimension_worst']
        ],
        theta=categories,
        fill='toself',
        name='Worst Value'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=False
    )

    return fig

def predictions(input_data):
    model = pickle.load(open('model/model.pkl', 'rb'))
    scaler = pickle.load(open('model/scaler.pkl', 'rb'))

    input_array = np.array(list(input_data.values())).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    
    if prediction[0]== 0:
        st.write('Benign')
    else:
        st.write('Malicious')
    
    
# This function loops through the dictionary, and for each item it takes
#  mininum and maximum values to scale them between 0-1
def scaled_values(input_dict):
    data = clean_data()

    X = data.drop(['diagnosis'], axis = 1)

    scaled_dict = {}

    for key, value in input_dict.items():
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value

    return scaled_dict


def main():
    st.set_page_config(
        page_title= 'Cancer Prediction',
        page_icon= ':female-doctor:',
        layout= 'wide',
        initial_sidebar_state= 'expanded',

    )

    with st.container():
        st.title('Breast Cancer Predictor')

    input_data = sidebar()

    col1, col2 = st.columns([4,1])  

    with col1:
        radar_chart= chart(input_data)
        st.plotly_chart(radar_chart)

    with col2:
        st.subheader('Cell cluster Prediction')
        st.write('The cell custer is: \n')
        predictions(input_data)
        st.write('The results generated by this tool should be interpreted by qualified medical practitioners and should not be considered as a definitive diagnosis.')


    
    
    

if __name__ == '__main__':
    main()