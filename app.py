from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    '''
        Cette méthode permet de prédire la classe d'une fleur en passant les features en paramètre à l'API
        request params: sepal_length, sepal_width, petal_length, petal_width
    '''
    sepal_length = request.args.get("sl", default=None, type=float)
    sepal_width  = request.args.get("sw", default=None, type=float)
    petal_length = request.args.get("pl", default=None, type=float)
    petal_width  = request.args.get("pw", default=None, type=float)

    # Check if any parameters is None
    if sepal_length is None or sepal_width is None or petal_length is None or petal_width is None:
        print("--> Missing parameter(s)") 
        return jsonify({'error': str("Missing parameter(s)")})
    
    # Load the machine learning model
    model = joblib.load("model_knn.pkl")

    # Predict the flower class
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(features)

    return jsonify({'prediction': str(prediction)})

if __name__ == '__main__':
    app.run(port=8000, debug=True)


