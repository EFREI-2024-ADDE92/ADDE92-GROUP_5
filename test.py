import requests
import random as r

nb = int(input("Nombre de tests aléatoires : "))

for i in range(1, nb):
    sl = r.uniform(0, 10)
    sw = r.uniform(0, 10)
    pl = r.uniform(0, 10)
    pw = r.uniform(0, 10)
    try:
        res = requests.get(f"https://groupe5-container-app.lemonflower-d97e6199.francecentral.azurecontainerapps.io/predict?sl={sl}&sw={sw}&pl={pl}&pw={pw}")
        print(res)
    except Exception as e:
        print("Exception: ", e)

try:
    res = requests.get(f"https://groupe5-container-app.lemonflower-d97e6199.francecentral.azurecontainerapps.io/metrics")
    print(res)
except Exception as e:
    print("Exception: ", e)