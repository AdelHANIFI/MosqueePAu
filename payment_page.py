from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QMovie
import requests
import time
import uuid

class PaymentPage(QWidget):
    def __init__(self, parent=None, amount=0.0, api_key=None, translations=None, current_language="fr"):
        super().__init__(parent)
        self.amount = amount
        self.api_key = api_key
        self.translations = translations if translations is not None else {}
        self.current_language = current_language
        self.token = None
        self.token_expiry = 0

        layout = QVBoxLayout()
        self.title = QLabel(self.translations.get(self.current_language, {}).get("payment_title", "JE SOUTIENS"))
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.title.setFont(QFont("Arial", 30, QFont.Bold))
        layout.addWidget(self.title)

        self.subtitle = QLabel(self.translations.get(self.current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setFont(QFont("Arial", 40, QFont.Bold))
        layout.addWidget(self.subtitle)

        self.amount_label = QLabel(f"{self.amount:.2f} €")
        self.amount_label.setAlignment(Qt.AlignCenter)
        self.amount_label.setFont(QFont("Arial", 50, QFont.Bold))
        layout.addWidget(self.amount_label)

        self.toggle_button = QPushButton("Cacher montant")
        self.toggle_button.setFont(QFont("Arial", 20))
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_visibility)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif = QMovie("C:/Users/AdelHANIFI/Desktop/mosquéé/borne-paiement/images/gif.gif")
        self.gif_label.setMovie(self.gif)
        self.gif.start()
        layout.addWidget(self.gif_label)

        self.instructions = QLabel("Veuillez taper ou insérer votre carte de crédit/débit ci-dessous")
        self.instructions.setAlignment(Qt.AlignCenter)
        self.instructions.setFont(QFont("Arial", 20))
        layout.addWidget(self.instructions)

        self.back_button = QPushButton("Retour")
        self.back_button.setFont(QFont("Arial", 20))
        self.back_button.clicked.connect(self.return_to_home)
        layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

        self.setLayout(layout)
        self.refresh_token()  

    def refresh_token(self):
        try:
            response = requests.post("https://api.sumup.com/token", data={
                "grant_type": "refresh_token",
                "refresh_token": "rt_classic_zV5UHdS5Fp0aQT4lCRSwAxeyQEwW6819llmyUcNfq2Kvz5abaIMIs",
                "client_id": "cc_classic_qf3ruSkctMqev5ZrWrhRViXFrj4he",
                "client_secret": "cc_sk_classic_mB997MTJmFEIcAbOJ0D2fGkfrfzRhQDmHUPtBCiqEQzaip4Wwu"
            })
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data['access_token']
                self.token_expiry = time.time() + token_data['expires_in']
            else:
                print("Erreur lors de la récupération du jeton :", response.json())
        except Exception as e:
            print("Erreur :", str(e))
        QTimer.singleShot(3500000, self.refresh_token)

    def initiate_payment(self, amount, donation_type):

        descriptions = {
        'iftar': 'Don pour l\'Iftar',
        'travaux': 'Don pour les travaux',
        'zakat': 'Zakat',
        'sadaqa': 'don pour la mosquée'
        }
        description = descriptions.get(donation_type, 'Don pour la mosquée')
    
        url = "https://api.sumup.com/v0.1/terminals/0af00839-2a15-413d-9c8e-584a5e58a72c/checkout"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        data = {"amount": amount,
                "currency": "EUR",
                "description": description,
                "external_reference": f"donation-{int(time.time())}",
                "client_id": str(uuid.uuid4())
                }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print("Paiement initié avec succès.")
                self.save_transaction(data)
            else:
                print("Erreur lors de l'initiation du paiement :", response.json())
        except Exception as e:
            print("Erreur :", str(e))

    def save_transaction(self, data):
        try:
            with open("transactions.txt", "a") as file:
                file.write(f"{time.ctime()}: {data}\n")
            print("Transaction enregistrée.")
        except Exception as e:
            print("Erreur lors de l'enregistrement de la transaction :", str(e))

    def cancel_payment(self):
        url = "https://api.sumup.com/v0.1/terminals/0af00839-2a15-413d-9c8e-584a5e58a72c/checkout/cancel"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 204:
                print("Paiement annulé avec succès.")
            else:
                print("Erreur lors de l'annulation :", response.json())
        except Exception as e:
            print("Une erreur est survenue lors de l'annulation :", str(e))
    def update_translations(self, translations, current_language):
        self.translations = translations
        self.current_language = current_language
        self.title.setText(self.translations.get(current_language, {}).get("payment_title", "JE SOUTIENS"))
        self.subtitle.setText(self.translations.get(current_language, {}).get("payment_subtitle", "Mosquée de Pau"))
        self.instructions.setText(self.translations.get(current_language, {}).get("payment_instructions", "Veuillez taper ou insérer votre carte de crédit/débit ci-dessous"))
    def toggle_visibility(self):
        if self.amount_label.text() == "******":
            self.amount_label.setText(f"{self.amount:.2f} €")
            self.toggle_button.setText("Cacher montant")
        else:
            self.amount_label.setText("******")
            self.toggle_button.setText("Afficher montant")

    def return_to_home(self):
        self.cancel_payment()
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)

    def set_amount(self, amount):
        self.amount = float(amount)
        self.amount_label.setText(f"{self.amount:.2f} €")
