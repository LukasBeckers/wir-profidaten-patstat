import pandas as pd
from pandas.io.formats.style_render import Optional
from fuzzywuzzy import process
from multiprocessing import Pool
from typing import List, Union
from typing import Optional as Opt
import re


def preprocess_names(name: str) -> str:
    name = name.lower()
    suffixes = [
          r'\bgmbh\b', r'\bag\b', r'\bllc\b', r'\binc\b', r'\bcorp\b', r'\bltd\b', r'\bco\b',
          r'\bs\.a\b', r'\bs\.r\.l\b', r'\bkg\b', r'\bohg\b', r'\bmbh\b', r'\bug\b', r'\bbv\b',
          r'\bnv\b', r'\bplc\b', r'\bse\b', r'\boy\b', r'\bkgaa\b', r'\bsc\b', r'\bs\.c\.a\b',
          r'\bs\.c\b', r'\bzrt\b', r'\bpte\b', r'\bsdn\b', r'\bbhd\b', r'\bco kg\b'
      ]

    pattern = r'(?i)\s?(' + '|'.join(suffixes) + r')\.?'
    cleaned_name = re.sub(pattern, '', name)

    return cleaned_name.strip()


class Patstat():
    csv_path = 'data/patstat_data.csv'
    data = pd.read_csv(csv_path)

    data["person_name"].apply(preprocess_names)

    @classmethod
    def show(cls):
        print(cls.data)


class Profidaten():
    excel_path = 'data/Profi-AuszugNov23_erweitert_V5.xlsx'
    data =  pd.read_excel(excel_path)

    @classmethod
    def show(cls):
        print(cls.data)


class AusführendeStelle(Profidaten):
    data = Profidaten.data["p_ausführendeStelle"].dropna()
    data.apply(preprocess_names)


class GemeindeKennziffer(Profidaten):
    data = Profidaten.data["p_gemeindekennzifferZE"].dropna()


def find_match(name, list_b:list, output_file: Opt[list]=None):
    print(f"start search for match for name: {name}")
    match = process.extractOne(name, list_b)
    print(f"Name: {name}, Match:{match}")

    if output_file is not None:
        with open(output_file, "a") as file:
            file.write(f"{name}; {match}\n")
    return match


class BestMatches(AusführendeStelle):
    @classmethod
    def find_closest_matches(cls, list_b: list, out_file: Opt[str]=None):

        with Pool(processes=20) as pool:
            matches = pool.starmap(find_match, [(name, list_b, out_file) for name in cls.data])

        cls.matches = matches


if __name__=="__main__":
    BestMatches.find_closest_matches(Patstat.data["person_name"])
