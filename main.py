from profidaten_patstat_matching import Patstat, Profidaten, BestMatches, AusführendeStelle


if __name__=="__main__":
    print(Patstat.data.shape)
    print(f'{len(Patstat.data["person_name"].dropna().drop_duplicates()) :,}')
    print(AusführendeStelle.data.shape)
    output_file = "./data/matching_results.txt"

    BestMatches.find_closest_matches(Patstat.data["person_name"].dropna().drop_duplicates(), out_file=output_file)
