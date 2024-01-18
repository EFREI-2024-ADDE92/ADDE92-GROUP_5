import requests
import random as r

nb = int(input("Nombre de tests aléatoires : "))

print("\n=========== TESTS PREDICTION ===========\n")
for i in range(0, nb):
    sl = r.uniform(0, 10)
    sw = r.uniform(0, 10)
    pl = r.uniform(0, 10)
    pw = r.uniform(0, 10)
    try:
        res = requests.get(f"https://groupe5-container-app.wonderfulrock-9d7f1fd9.francecentral.azurecontainerapps.io/predict?sl={sl}&sw={sw}&pl={pl}&pw={pw}")
        print(f"{i+1}. {res.json().get('prediction')}")
    except Exception as e:
        print("Exception 1: ", e)

print("\n============ TESTS METRICS =============\n")
try:
    res = requests.get(f"https://groupe5-container-app.wonderfulrock-9d7f1fd9.francecentral.azurecontainerapps.io/metrics")
    print(res.text)
except Exception as e:
    print("Exception 2: ", e)