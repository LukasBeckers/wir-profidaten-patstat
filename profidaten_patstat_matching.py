import pandas as pd
from fuzzywuzzy import process
from multiprocessing import Pool




class Patstat():
    csv_path = 'data/patstat_data.csv'
    data = pd.read_csv(csv_path)

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


class GemeindeKennziffer(Profidaten):
    data = Profidaten.data["p_gemeindekennzifferZE"].dropna()


def find_match(name, list_b):
    print(f"start search for match for name: {name}")
    match = process.extractOne(name, list_b)
    print(f"Name: {name}, Match:{match}")
    return match


class BestMatches(AusführendeStelle):
    @classmethod
    def find_closest_matches(cls, list_b: list):

        with Pool(processes=10) as pool:
            matches = pool.starmap(find_match, [(name, list_b) for name in cls.data])

        cls.matches = matches


if __name__=="__main__":
    BestMatches.find_closest_matches(Patstat.data["person_name"])
