import pandas as pd
from pandas.io.formats.style_render import Optional
from fuzzywuzzy import process
from multiprocessing import Pool
from typing import List, Union, Dict
from typing import Optional as Opt

from preprocessing import SimpleGMBHRemover


class Patstat:
    csv_path = "data/patstat_data.csv" # Change this if needed
    data = pd.read_csv(csv_path)
    data = data[data["applt_seq_nr"] != 0]

    @classmethod
    def show(cls):
        print(cls.data)


class Profidaten:
    excel_path = "./data/Profi-Auszug 02.08.2024.xlsx" # Change this if needed
    data = pd.read_excel(excel_path)

    @classmethod
    def show(cls):
        print(cls.data)


class AusführendeStelle(Profidaten):
    data = Profidaten.data["p_ausführendeStelle"].dropna()
    data = (
        pd.Series([SimpleGMBHRemover.preprocess_name(name) for name in data])
        .drop_duplicates()
        .tolist()
    )


class GemeindeKennziffer(Profidaten):
    data = Profidaten.data["p_gemeindekennzifferZE"].dropna()


def find_match(name, list_b: list, output_file: Opt[list] = None):
    print(f"start search for match for name: {name}")
    match = process.extractOne(name, list_b)
    print(f"Name: {name}, Match:{match}")

    if output_file is not None:
        with open(output_file, "a") as file:
            file.write(f"{name}; {match}\n")
    return match


def load_clean_names_dict(file_path) -> Dict[str, str]:
    clean_names_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            name, clean_name = line.split(";")
            clean_names_dict[name] = clean_name
    return clean_names_dict


class BestMatches(AusführendeStelle):
    @classmethod
    def find_closest_matches(cls, list_b: list, out_file: Opt[str] = None):

        with Pool(processes=20) as pool:
            matches = pool.starmap(
                find_match, [(name, list_b, out_file) for name in cls.data]
            )

        cls.matches = matches


if __name__ == "__main__":
    pass
