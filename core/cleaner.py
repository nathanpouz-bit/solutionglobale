import pandas as pd

# -----------------------------
# Nettoyage d'une colonne texte → numérique
# -----------------------------
def clean_numeric_column(df, col):

    df[col] = (
        df[col]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# -----------------------------
# Nettoyage des colonnes texte
# -----------------------------
def clean_text_column(df, col):

    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return df


# -----------------------------
# Nettoyage global du dataset
# -----------------------------
def clean_data(df):

    # colonnes numériques fréquentes
    numeric_cols = ["Sales", "Profit", "Units Sold", "COGS", "Discounts"]

    for col in numeric_cols:
        if col in df.columns:
            df = clean_numeric_column(df, col)

    # colonnes texte fréquentes
    text_cols = ["Country", "Product", "Segment"]

    for col in text_cols:
        if col in df.columns:
            df = clean_text_column(df, col)

    # gestion des dates
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # suppression des lignes complètement vides
    df = df.dropna(how="all")

    return df
