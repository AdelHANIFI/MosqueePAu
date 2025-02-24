import sqlite3

def init_db():
    """
    Initialise la base de données en créant la table 'dons' si elle n'existe pas.
    """
    conn = sqlite3.connect("dons.db")
    cursor = conn.cursor()

    # Création de la table 'dons'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie TEXT NOT NULL,
            montant REAL NOT NULL,
            date_don TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def ajouter_don(categorie, montant):
    """
    Ajoute un don dans la base de données.
    """
    conn = sqlite3.connect("dons.db")
    cursor = conn.cursor()

    # Insertion du don
    cursor.execute("""
        INSERT INTO dons (categorie, montant)
        VALUES (?, ?)
    """, (categorie, montant))

    conn.commit()
    conn.close()

def recuperer_dons_par_categorie(categorie):
    """
    Récupère les dons d'une catégorie donnée.
    """
    conn = sqlite3.connect("dons.db")
    cursor = conn.cursor()

    # Requête pour récupérer les dons
    cursor.execute("""
        SELECT * FROM dons WHERE categorie = ? ORDER BY date_don DESC
    """, (categorie,))
    dons = cursor.fetchall()

    conn.close()
    return dons
