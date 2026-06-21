import pandas as pd


# -----------------------------
# Nettoyage numérique
# -----------------------------
def clean_numeric_column(df, col):

    df[col] = (
        df[col]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("£", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


# -----------------------------
# Nettoyage texte
# -----------------------------
def clean_text_column(df, col):

    df[col] = df[col].astype(str).str.strip().str.lower()

    return df


# -----------------------------
# Détection intelligente du type de colonne
# -----------------------------
def detect_column_type(col_name, sample_values, full_series):

    # -----------------------------
    # 1. DETECTION ID (basée sur les données)
    # -----------------------------
    full_series = full_series.dropna()

    if len(full_series) > 0:

        unique_ratio = len(full_series.unique()) / len(full_series)
        avg_length = full_series.astype(str).str.len().mean()

        # si presque unique + valeurs courtes/moyennes → ID
        if unique_ratio > 0.9 and avg_length < 40:
            return "id"

    # -----------------------------
    # 2. DETECTION NUMÉRIQUE
    # -----------------------------
    numeric_score = 0

    for v in sample_values:
        v = str(v).replace(",", "").replace("€", "").replace("$", "").strip()

        if v.replace(".", "").isdigit():
            numeric_score += 1

    if len(sample_values) > 0 and numeric_score >= len(sample_values) / 2:
        return "numeric"

    # -----------------------------
    # 3. PAR DÉFAUT = TEXTE
    # -----------------------------
    return "text"


# -----------------------------
# CLEAN GLOBAL DATASET
# -----------------------------
def clean_data(df):

    for col in df.columns:

        # ignorer colonnes totalement vides
        if df[col].isnull().all():
            continue

        sample = df[col].dropna().astype(str).head(10)

        col_type = detect_column_type(col, sample, df[col])

        # -----------------------------
        # NUMERIC
        # -----------------------------
        if col_type == "numeric":
            df = clean_numeric_column(df, col)

        # -----------------------------
        # TEXT
        # -----------------------------
        elif col_type == "text":
            df = clean_text_column(df, col)

        # -----------------------------
        # ID (barcode, SKU, etc.)
        # -----------------------------
        elif col_type == "id":
            df[col] = df[col].astype(str).str.strip()

    # -----------------------------
    # DATES AUTO-DETECTION
    # -----------------------------
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # -----------------------------
    # SUPPRESSION LIGNES VIDES
    # -----------------------------
    df = df.dropna(how="all")

    return df
