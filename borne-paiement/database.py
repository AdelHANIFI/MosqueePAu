import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="mosquee.db"):
        """
        Initialise la connexion à la base de données SQLite et crée les tables nécessaires.
        """
        self.conn = sqlite3.connect(db_name)
        self.create_transactions_table()

    def create_transactions_table(self):
        """
        Crée la table des transactions si elle n'existe pas déjà.
        """
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            category TEXT,
            amount REAL,
            adherent_id INTEGER NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_transaction(self, transaction_type, category, amount, adherent_id=None):
        """
        Ajoute une nouvelle transaction dans la base de données.

        Args:
            transaction_type (str): Le type de la transaction (ex. : Don, Ramadan, Adhérent).
            category (str): La catégorie de la transaction (ex. : Général, Iftar).
            amount (float): Le montant de la transaction.
            adherent_id (int, optional): L'ID de l'adhérent (si applicable).
        """
        query = """
        INSERT INTO transactions (date, type, category, amount, adherent_id)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), transaction_type, category, amount, adherent_id))
        self.conn.commit()

    def get_transactions(self):
        """
        Récupère toutes les transactions enregistrées, triées par date.

        Returns:
            list: Une liste de tuples contenant les transactions.
        """
        query = "SELECT * FROM transactions ORDER BY date DESC"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def export_transactions_to_csv(self, filename="transactions.csv"):
        """
        Exporte les transactions au format CSV.

        Args:
            filename (str): Le nom du fichier CSV à créer.
        """
        transactions = self.get_transactions()
        with open(filename, "w", encoding="utf-8") as file:
            # Écrire l'en-tête
            file.write("Date,Type,Category,Amount,Adherent ID\n")
            # Écrire chaque transaction
            for transaction in transactions:
                file.write(",".join(map(str, transaction[1:])) + "\n")

    def get_transactions_by_category(self, category):
        """
        Récupère les transactions pour une catégorie donnée.

        Args:
            category (str): La catégorie à filtrer.

        Returns:
            list: Une liste de tuples contenant les transactions correspondant à la catégorie.
        """
        query = "SELECT * FROM transactions WHERE category = ? ORDER BY date DESC"
        cursor = self.conn.execute(query, (category,))
        return cursor.fetchall()

    def get_total_amount_by_category(self, category):
        """
        Calcule le montant total des transactions pour une catégorie donnée.

        Args:
            category (str): La catégorie à filtrer.

        Returns:
            float: Le montant total pour la catégorie.
        """
        query = "SELECT SUM(amount) FROM transactions WHERE category = ?"
        cursor = self.conn.execute(query, (category,))
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()


if __name__ == "__main__":
    db = Database()

    # Ajouter des exemples de transactions
    db.add_transaction("Don", "Travaux", 50.0)
    db.add_transaction("Ramadan", "Iftar", 30.0)
    db.add_transaction("Adhérent", "Recharge", 20.0, adherent_id=12345)

    # Afficher toutes les transactions
    print("Toutes les transactions :")
    for transaction in db.get_transactions():
        print(transaction)

    # Exporter les transactions en CSV
    db.export_transactions_to_csv()

    # Afficher les transactions par catégorie
    print("\nTransactions pour la catégorie 'Travaux' :")
    for transaction in db.get_transactions_by_category("Travaux"):
        print(transaction)

    # Calculer le total pour une catégorie
    total = db.get_total_amount_by_category("Travaux")
    print(f"\nTotal pour la catégorie 'Travaux' : {total} €")

    # Fermer la connexion
    db.close()
