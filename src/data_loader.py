import pandas as pd


def clean_dataset(df):
    df = df.copy()

    df.columns = ["label", "message"]

    df["label"] = (
        df["label"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    df["message"] = (
        df["message"]
        .astype(str)
        .str.strip()
    )

    df = df[df["label"].isin(["ham", "spam"])]
    df = df[df["message"] != ""]

    df = df.drop_duplicates()

    return df.reset_index(drop=True)


def load_dataset(filepath):

    try:
        if filepath.endswith(".tsv"):
            df = pd.read_csv(
                filepath,
                sep="\t",
                names=["label", "message"]
            )
        else:
            df = pd.read_csv(filepath)
    except UnicodeDecodeError:
        if filepath.endswith(".tsv"):
            df = pd.read_csv(
                filepath,
                sep="\t",
                names=["label", "message"],
                encoding="latin-1"
            )
        else:
            df = pd.read_csv(filepath, encoding="latin-1")

    if "v1" in df.columns and "v2" in df.columns:
        df = df[["v1", "v2"]]
        df.columns = ["label", "message"]
    elif "label" in df.columns and "message" in df.columns:
        df = df[["label", "message"]]
    elif "Category" in df.columns and "Message" in df.columns:
        df = df[["Category", "Message"]]
        df.columns = ["label", "message"]

    return clean_dataset(df)
