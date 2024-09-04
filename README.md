# WIR Profidaten Patstat Matching
In this Project the organizational data from the "Profi" dataset is matched to datapoints from the "Patstat" dataset.

To match datapoints, the "Ausführende Stelle" from the Profi dataset is matched to "person_name" from the Patstat database via string similarity.

## Prerequisites

OpenAI API Key

Patstat dataset in form of a csv file including all applicants from an area you want to match (in this case germany)
The following columns must be included: ("applt_seq_nr", "person_name", "person_id")

Profi dataset in form of a xlsx file.
The following columns must be included: ("ID", "p_ausführendeStelle", "p_gemeindekennzifferZE")

## Getting Started

Install the requirements.txt file.

```
pip install -r requirements.txt
```

Copy your Patstat dataset csv and your "profi" dataset csv into /data.

Change the excel_path and the csv_path to match the file names in the profidaten_patstat_matching.py

```
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
```

Add your openAI api key in main.ipynb in section "Classifing the Matching Results using gpt-4o mini"

You may need to install a new ipykernel with all requirements installed before you can run the  main.ipynb notebook.
To do this create a venv install the requirements.txt into it and then install the ipykernel into the venv and start the jupyter notebook

Create the venv
```
python3 -m venv venv
```

activate the venv in Linux
```
# Linux
source venv/bin/activate
```
activate the venv in Windows
```
# Windows
call venv\Scripts\activate
```

Install the requirements and the ipykernel
```
pip install -r requirements.txt
pip install ipykernel
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```
Start Jupyter Notebook
```
jupyter notebook
```

To perform the matching Run all cells of main.ipynb.

The result files will be found in the /data dir.
