from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class DonsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurer le layout de la page des dons
        layout = QVBoxLayout()

        # Titre de la page
        title = QLabel("Dons pour la Mosquée")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 30, QFont.Bold))

        # Message explicatif
        explanation = QLabel("Choisissez un montant à donner pour soutenir la mosquée.")
        explanation.setAlignment(Qt.AlignCenter)
        explanation.setFont(QFont("Arial", 14))

        # Boutons pour les montants prédéfinis
        buttons_layout = QVBoxLayout()

        for montant in [5, 10, 20, 50, 100]:  # Montants prédéfinis
            button = QPushButton(f"{montant} €")
            button.setFont(QFont("Arial", 18))
            button.setMinimumHeight(50)
            buttons_layout.addWidget(button)

        # Bouton retour
        back_button = QPushButton("Retour")
        back_button.setFont(QFont("Arial", 16))
        back_button.setMinimumHeight(50)
        back_button.clicked.connect(self.return_to_home)

        # Ajouter les widgets au layout principal
        layout.addWidget(title)
        layout.addWidget(explanation)
        layout.addLayout(buttons_layout)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def return_to_home(self):
        """
        Retourne à la page d'accueil.
        """
        parent = self.parent()
        if parent:
            parent.setCurrentIndex(0)  # Affiche la page d'accueil
