import requests
import random as r

nb = int(input("Nombre de tests aléatoires : "))

PRO_URL = "https://groupe5-newcontainer-app.politewater-20dc8a0f.francecentral.azurecontainerapps.io"
DEV_URL = "http://127.0.0.1:80"

BASE_URL = DEV_URL

print("\n=========== TESTS PREDICTION ===========\n")
for i in range(0, nb):
    sl = r.uniform(0, 10)
    sw = r.uniform(0, 10)
    pl = r.uniform(0, 10)
    pw = r.uniform(0, 10)
    try:
        res = requests.get(f"{BASE_URL}/predict?sl={sl}&sw={sw}&pl={pl}&pw={pw}")
        print(f"\n-> Prediction {i+1}")
        print(f"-> Params:\n\tSepal length: {sl}\n\tSepal width: {sw}\n\tPetal length: {pl}\n\tPetal width: {sw}")
        print(f"-> Result: {res.json().get('prediction')}")
    except Exception as e:
        print("Exception 1: ", e)

print("\n============ TESTS METRICS =============\n")
try:
    res = requests.get(f"{BASE_URL}/metrics")
    print(res.text)
except Exception as e:
    print("Exception 2: ", e)