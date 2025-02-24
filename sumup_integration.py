import requests

class SumUpIntegration:
    def __init__(self, api_key,merchant_code):
        self.api_key = api_key
        self.merchant_code = merchant_code
        self.base_url = "https://api.sumup.com/v0.1"  # Assurez-vous d'utiliser l'URL correcte

    def start_payment(self, amount, currency="EUR"):
        url = f"{self.base_url}/checkouts"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount,
            "currency": currency,
            "pay_to_email": "5cd93e3618d9412f816fd54c39df97c8@developer.sumup.com",  # Remplacez par l'email de votre compte SumUp
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            if response.status_code == 200 or response.status_code == 201:
                print("Paiement initié :", response_data)
                return response_data
            else:
                print("Erreur lors de la requête SumUp:", response_data)
                return None
        except Exception as e:
            print("Erreur lors de l'initialisation du paiement.", e)
            return None


    def pair_terminal(self, pairing_code):
        """
        Pairer le terminal SumUp avec le compte marchand.
        """
        url = f"{self.base_url}/merchants/{self.merchant_code}/readers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {"pairing_code": pairing_code}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print("Réponse de l'API :", response.json())
            return response.json()  # Retourne les détails du terminal pairé
        except requests.RequestException as e:
            print("Erreur lors du pairing avec le terminal :", e)
            return None