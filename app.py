from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, generate_latest, REGISTRY
import joblib
import numpy as np
#
app = Flask(__name__)
#
api_call_counter = Counter('api_calls_total', 'Total number of API calls')
#
# Add prometheus_client metric with labels
iris_setosa_predictions_total = Counter(
    'setosa_predictions_total',
    'Total number of Iris Setosa predictions',
    labelnames=['endpoint', 'predictions'],
    namespace='api',
)
iris_virginica_predictions_total = Counter(
    'virginica_predictions_total',
    'Total number of Iris Virginica predictions',
    labelnames=['endpoint', 'predictions'],
    namespace='api',
)
iris_versicolor_predictions_total = Counter(
    'versicolor_predictions_total',
    'Total number of Iris Versicolor predictions',
    labelnames=['endpoint', 'predictions'],
    namespace='api',
)
#
# Load the machine learning model 
model = joblib.load("model_knn.pkl")
#
#
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({'Message': str("Bonjour! Appelez l'api /predict avec les paramètres: sl (sepal lenght), sw (sepal width), pl (petal lenght), pw (petal width).")})
#
@app.route('/metrics')
def metrics():
    return Response(generate_latest(REGISTRY), mimetype='text/plain')
#
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

    # Predict the flower class
    features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(features)[0]

    # Enregistrez l'appel dans le compteur
    api_call_counter.inc()

    # Mettez à jour les compteurs pour chaque classe en fonction de la prédiction
    if prediction == 'Iris-setosa':
        iris_setosa_predictions_total.labels(endpoint='/predict', predictions=str(prediction)).inc()
    elif prediction == 'Iris-virginica':
        iris_virginica_predictions_total.labels(endpoint='/predict', predictions=str(prediction)).inc()
    elif prediction == 'Iris-versicolor':
        iris_versicolor_predictions_total.labels(endpoint='/predict', predictions=str(prediction)).inc()

    return jsonify({'prediction': str(prediction)})
#
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)


