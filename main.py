import pandas as pd
import requests


def read_data(filename:str)->pd.DataFrame:
    with open(filename, "r", encoding="utf-8") as file:
        data = pd.read_json(file, orient="index", lines=True, nrows=10)
    return data




if __name__ == "__main__":
    data = read_data("cxdb_5d42c72a9450811eb91d419a054c185c.messages.json")
    print(data.head())
