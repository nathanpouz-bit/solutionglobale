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
# Détection du type de colonne
# -----------------------------
def detect_column_type(col_name, sample_values):

    name = col_name.lower()

    # 🔴 IDENTIFIANTS (barcode, id, sku, etc.)
    if any(key in name for key in ["id", "code", "barcode", "sku", "ref"]):
        return "id"

    # 🟡 TEXTES CLASSIQUES
    if any(key in name for key in ["country", "product", "segment", "name", "supplier"]):
        return "text"

    # 🟢 TEST NUMÉRIQUE
    numeric_score = 0

    for v in sample_values:
        v = str(v).replace(",", "").replace("€", "").replace("$", "").strip()
        if v.replace(".", "").isdigit():
            numeric_score += 1

    if len(sample_values) > 0 and numeric_score >= len(sample_values) / 2:
        return "numeric"

    return "text"


# -----------------------------
# CLEANING GLOBAL
# -----------------------------
def clean_data(df):

    for col in df.columns:

        # ignorer colonnes totalement vides
        if df[col].isnull().all():
            continue

        sample = df[col].dropna().astype(str).head(10)

        col_type = detect_column_type(col, sample)

        # NUMÉRIQUE
        if col_type == "numeric":
            df = clean_numeric_column(df, col)

        # TEXTE
        elif col_type == "text":
            df = clean_text_column(df, col)

        # ID / CODE BARRE
        elif col_type == "id":
            df[col] = df[col].astype(str).str.strip()

    # -----------------------------
    # DATES (auto-détection simple)
    # -----------------------------
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # -----------------------------
    # SUPPRESSION LIGNES VIDES
    # -----------------------------
    df = df.dropna(how="all")

    return df
