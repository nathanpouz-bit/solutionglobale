import pandas as pd

# -----------------------------
# Lecture Excel
# -----------------------------
def load_excel(file):
    df = pd.read_excel(file)
    return df


# -----------------------------
# Saisie manuelle → DataFrame
# -----------------------------
def load_manual(data_dict):
    """
    data_dict = dictionnaire ou ligne saisie utilisateur
    """
    df = pd.DataFrame([data_dict])
    return df


# -----------------------------
# Fonction principale (entrée unique)
# -----------------------------
def load_data(source_type, data):
    """
    source_type = "excel" ou "manual"
    data = fichier ou dictionnaire
    """

    if source_type == "excel":
        df = load_excel(data)

    elif source_type == "manual":
        df = load_manual(data)

    else:
        raise ValueError("Type de source inconnu")

    return df
