import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QComboBox, QStackedWidget
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from dons_page import DonsPage


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borne de Paiement - Mosquée de Pau")
        self.showFullScreen()  # Fenêtre en plein écran

        # Traductions
        self.current_language = "fr"
        self.translations = self.load_translations()

        # Créer un gestionnaire de pages
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        # Charger le fichier de styles
        self.apply_styles()

        # Ajouter les pages
        self.home_page = self.create_home_page()
        self.dons_page = DonsPage()

        # Ajouter les pages au gestionnaire
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.dons_page)

        # Afficher la page d'accueil par défaut
        self.pages.setCurrentWidget(self.home_page)
    def load_translations(self):
        """
        Charge les traductions.
        """
        return {
            "fr": {
                "title": "Je soutiens la Mosquée de Pau",
                "adherents": "Espace Adhérents",
                "adherents_help": "Rechargez votre carte d'adhérent",
                "mosque": "Dons pour la mosquée",
                "mosque_help": "Aidez la mosquée à fonctionner",
                "works": "Travaux de la mosquée",
                "works_help": "Soutenez les rénovations et les projets",
                "ramadan": "Ramadan",
                "ramadan_help": "Dons pour l'Iftar et la Zakât al-Fitr",
                "footer": "Edited by @adelhanifi",
                "language_label": "Langue :"
            },
            "en": {
                "title": "I support the Mosque of Pau",
                "adherents": "Members Area",
                "adherents_help": "Recharge your membership card",
                "mosque": "Donations \nfor the mosque",
                "mosque_help": "Support the mosque's operations",
                "works": "Mosque Renovation",
                "works_help": "Support renovations and projects",
                "ramadan": "Ramadan",
                "ramadan_help": "Donations for Iftar and Zakât al-Fitr",
                "footer": "Edited by @adelhanifi",
                "language_label": "Language:"
            },
            "ar": {
                "title": "أدعم مسجد بو",
                "adherents": "فضاء الأعضاء",
                "adherents_help": "أعد شحن بطاقة العضو الخاصة بك",
                "mosque": "تبرعات للمسجد",
                "mosque_help": "ساعد في تشغيل المسجد",
                "works": "أعمال المسجد",
                "works_help": "دعم التجديدات والمشاريع",
                "ramadan": "رمضان",
                "ramadan_help": "تبرعات للإفطار وزكاة الفطر",
                "footer": "من إعداد @adelhanifi",
                "language_label": "اللغة:"
            },
        }


    def apply_styles(self):
        """
        Charge le fichier de styles QSS.
        """
        try:
            with open("C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\templates\\styles.qss", "r") as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print("Le fichier styles.qss est introuvable. Veuillez vérifier son emplacement.")

    def create_home_page(self):
        """
        Configure la page d'accueil.
        """
        main_widget = QWidget()
        layout = QVBoxLayout()

        # Barre de sélection de langue
        language_layout = QHBoxLayout()
        language_layout.addStretch()

        language_label = QLabel(self.translations[self.current_language]["language_label"])
        language_label.setFont(QFont("Arial", 12))
        language_layout.addWidget(language_label)

        self.language_selector = QComboBox()
        self.language_selector.addItems(["Français", "English", "العربية"])
        self.language_selector.currentIndexChanged.connect(self.change_language)
        language_layout.addWidget(self.language_selector)

        language_layout.addStretch()
        layout.addLayout(language_layout)

        # Logo
        logo = QLabel()
        logo_pixmap = QPixmap("C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\images\\mosquee_logo.png").scaled(
            250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)

        # Titre
        title = QLabel(self.translations[self.current_language]["title"])
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 40, QFont.Bold))

        # Boutons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(40)
        buttons = [
            {"key": "adherents", "help_key": "adherents_help", "icon": "C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\images\\adherents_icon.png"},
            {"key": "mosque", "help_key": "mosque_help", "icon": "C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\images\\mosquee_icon.png"},
            {"key": "works", "help_key": "works_help", "icon": "C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\images\\travaux_icon.png"},
            {"key": "ramadan", "help_key": "ramadan_help", "icon": "C:\\Users\\AdelHANIFI\\Desktop\\mosquéé\\borne-paiement\\images\\ramadan_icon.png"},
        ]
        self.buttons = []

        for button_data in buttons:
            button_layout = QVBoxLayout()

            # Icône
            icon_label = QLabel()
            icon_pixmap = QPixmap(button_data["icon"]).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)
            icon_label.setAlignment(Qt.AlignCenter)

            # Texte
            text_label = QLabel(self.translations[self.current_language][button_data["key"]])
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setFont(QFont("Arial", 27, QFont.Bold))

            help_label = QLabel(self.translations[self.current_language][button_data["help_key"]])
            help_label.setAlignment(Qt.AlignCenter)
            help_label.setFont(QFont("Arial", 14))
            help_label.setStyleSheet("color: gray;")
            # Ajouter l'icône et le texte
            # Ajouter les éléments au layout
            button_layout.addWidget(icon_label)
            button_layout.addWidget(text_label)
            button_layout.addWidget(help_label)


            # Bouton conteneur
            button_container = QPushButton()
            button_container.setLayout(button_layout)
            button_container.setMinimumSize(200, 200)

            # Connecter le bouton au gestionnaire
            button_container.clicked.connect(self.handle_mosque)

            buttons_layout.addWidget(button_container)

        # Ajouter les widgets au layout principal
        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addLayout(buttons_layout)

        main_widget.setLayout(layout)
        return main_widget

    def handle_mosque(self):
        """
        Gère la redirection vers la page des dons.
        """
        self.pages.setCurrentWidget(self.dons_page)

    def change_language(self):
        """
        Change la langue de l'interface.
        """
        languages = {"Français": "fr", "English": "en", "العربية": "ar"}
        selected_language = self.language_selector.currentText()
        self.current_language = languages[selected_language]


        # Mettre à jour les textes
        self.title.setText(self.translations[self.current_language]["title"])
        self.footer.setText(self.translations[self.current_language]["footer"])
        for text_label, help_label, key, help_key in self.buttons:
            text_label.setText(self.translations[self.current_language][key])
            help_label.setText(self.translations[self.current_language][help_key])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
