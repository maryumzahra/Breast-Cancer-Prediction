import pandas as pd
from sklearn.preprocessing import StandardScaler  
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle


def create_model(data):
    X = data.drop(['diagnosis'], axis = 1)  #features on which predictions depends on
    y = data['diagnosis']  #prediction

    # Scale data
    scaler = StandardScaler()
    X = scaler.fit_transform(X) 

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size= 0.2, random_state= 42
    )

    # train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # test model
    y_pred = model.predict(X_test)
    print('Model accuracy: ', accuracy_score(y_test, y_pred))
    print('Classification report:\n', classification_report(y_test, y_pred))
    return model, scaler




def clean_data():
    data= pd.read_csv('data/data.csv')
    
    # Drop unnecessary columns
    data = data.drop(['Unnamed: 32', 'id'], axis = 1)
    data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})
    return data




def main():
    data = clean_data()
    model, scaler = create_model(data)

    # Pickling
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('model/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)


if __name__ == '__main__':
    main()