import os
import openai
import pandas as pd


def load_matching_results(file_path:str) -> pd.DataFrame:
    data = pd.read_csv(file_path, delimiter=";", lineterminator="\n")
    # removing the confindence scores from the results, they may be used later though.
    data["Patstat"] = data["Patstat"].apply(lambda datapoint: datapoint.split("'")[1].strip("\n"))

    return data


def classify_matching_results(name0: str, name1: str) -> bool:
    """
    Uses an openai chat model to classify string-matching results into matching or unmatching
    """

    api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = api_key
    model = os.getenv("MODEL")

    system_prompt = {
      "role": "system",
      "content": """You are an AI model designed to evaluate the correctness of string matching between two organization-names. Your task is to determine whether the two provided names match correctly or not. If the same organization is mentioned, but not the correct subdepartemnt, the results should be "True" anyway. Minor typos are also no reason for a disqualifiacition. Only if it is not clearly visible that the same organizations are mentioned the result should be "False" The input format will always be: "Name1: <name1>; Name2: <name2>

      Instructions:

          Compare the two names provided in the input.
          Consider the names a match if they refer to the same entity, even if there are minor variations, such as capitalization, spacing, or common abbreviations.
          Return "True" if the names correctly match.
          Return "False" if the names do not match.
          Provide only "True" or "False" as the output, without any additional information."""
    }

    prompt_example0 = {"role": "user",
        "content": f"Name1: daberkower landhof; Name2: h+h &"
    }
    response_example0 = {"role": "assistant", "content": "False"}

    prompt_example1 = {"role": "user",
        "content": f"Name1: roboscreen; Name2: roboscreen"
    }
    response_example1 = {"role": "assistant", "content": "True"}

    prompt_example2 = {"role": "user",
        "content": f"Name1: martin-luther-universität halle-wittenberg - medizinische fakultät und universitätsklinikum - department für innere medizin - versorgungsforschung - pflege im krankenhaus; Name2:  martin-luther-universität halle-wittenberg"
    }
    response_example2 = {"role": "assistant", "content": "True"}

    prompt_example3 = {"role": "user",
        "content": f"Name1: leibniz institut für katalyse; Name2:  leibnitz institut für katalyse"
    }
    response_example3 = {"role": "assistant", "content": "True"}

    prompt = {"role": "user",
        "content": f"Name1: {name0}, Name2: {name1}"
    }
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                system_prompt,
                prompt_example0,
                response_example0,
                prompt_example1,
                response_example1,
                prompt_example2,
                response_example2,
                prompt_example3,
                response_example3,
                prompt
            ],
            max_tokens=3
        )
    except Exception:
        return classify_matching_results(name0, name1)

    response = response['choices'][0]['message']['content'].strip()
    return response


if __name__=="__main__":
    pass
    api_key = os.getenv('OPENAI_API_KEY')
    print(api_key)