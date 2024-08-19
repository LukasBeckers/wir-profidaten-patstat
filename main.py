from profidaten_patstat_matching import Patstat, Profidaten, BestMatches, AusführendeStelle


if __name__=="__main__":
    print(Patstat.data.shape)
    print("Patstat")
    print(Patstat.data["person_name"].dropna().drop_duplicates()[:100])
    print("Ausführende Stelle")
    print(AusführendeStelle.data[:100])
    output_file = "./data/matching_results_cleaned.txt"
    with open (output_file, "a") as file:
        file.write("Name; Match")

    BestMatches.find_closest_matches(Patstat.data["person_name"].dropna().drop_duplicates(), out_file=output_file)
