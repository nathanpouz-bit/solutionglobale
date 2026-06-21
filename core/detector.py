import pandas as pd


# -----------------------------
# DETECTION DU TYPE DE DATASET
# -----------------------------
def detect_dataset_type(df):

    cols = [c.lower() for c in df.columns]

    # -------------------------
    # SCORE VENTES
    # -------------------------
    sales_keywords = ["sales", "revenue", "profit", "turnover", "gross"]

    sales_score = sum(
        any(k in col for k in sales_keywords)
        for col in cols
    )

    # -------------------------
    # SCORE ACHATS
    # -------------------------
    purchase_keywords = ["purchase", "cost", "supplier", "buy", "expense"]

    purchase_score = sum(
        any(k in col for k in purchase_keywords)
        for col in cols
    )

    # -------------------------
    # DECISION
    # -------------------------
    if sales_score > purchase_score:
        return "sales"

    elif purchase_score > sales_score:
        return "purchases"

    else:
        return "unknown"


# -----------------------------
# DETECTION DES COLONNES KPI
# -----------------------------
def detect_kpi_columns(df):

    cols = {c.lower(): c for c in df.columns}

    mapping = {
        "sales": None,
        "profit": None,
        "cost": None,
        "quantity": None
    }

    for col in cols:

        if "sales" in col or "revenue" in col:
            mapping["sales"] = cols[col]

        elif "profit" in col:
            mapping["profit"] = cols[col]

        elif "cost" in col or "cogs" in col:
            mapping["cost"] = cols[col]

        elif "unit" in col or "quantity" in col:
            mapping["quantity"] = cols[col]

    return mapping


# -----------------------------
# FONCTION PRINCIPALE
# -----------------------------
def analyze_dataset(df):

    dataset_type = detect_dataset_type(df)
    kpi_mapping = detect_kpi_columns(df)

    return {
        "type": dataset_type,
        "mapping": kpi_mapping
    }
