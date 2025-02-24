import requests

CLIENT_ID = "cc_classic_qf3ruSkctMqev5ZrWrhRViXFrj4he"
CLIENT_SECRET = "cc_sk_classic_mB997MTJmFEIcAbOJ0D2fGkfrfzRhQDmHUPtBCiqEQzaip4Wwu"

url = "https://api.sumup.com/token"

payload = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, data=payload, headers=headers)

if response.status_code == 200:
    token = response.json()["access_token"]
    print("Jeton d'accès :", token)
else:
    print("Erreur lors de la récupération du jeton :", response.json())
