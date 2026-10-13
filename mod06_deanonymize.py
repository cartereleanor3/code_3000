import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    values = ["age", "zip3", "gender"]
    names = aux_df[~aux_df.duplicated(subset=values, keep=False)]
    ids = anon_df[~anon_df.duplicated(subset=values, keep=False)]
    merged = names.merge(ids, on=values, how="inner", validate="one_to_one")
    matches = merged[["anon_id", "name"]].copy().rename(columns={"name": "matched_name"})
    return matches

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df)/len(anon_df)

load_data_input = 'mod06_data/anonymized.csv', 'mod06_data/auxiliary.csv'
matches_df = link_records(*load_data(*load_data_input))

print(deanonymization_rate(matches_df, load_data(*load_data_input)[0]))
