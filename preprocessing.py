import re
import openai
import os
from typing import Dict, Union
import time
from typing import List


class NamePreprocessor:
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    model = os.getenv("MODEL")


class GMBHRemover(NamePreprocessor):
    system_prompt = {
        "role": "system",
        "content": "You are an AI agent specialized in cleaning and standardizing company names. Your primary task is to remove any legal identifiers or suffixes commonly associated with company types from company names. These identifiers include, but are not limited to, terms like GmbH, AG, Ltd, Inc, LLC, and S.A. Your goal is to provide a clean company name that excludes these legal designations while retaining the core brand name. Ensure that the names are returned in a consistent format, without any extra spaces or punctuation that may result from the removal process. If the provided name is not a company or public institution (like a University) but the name of an idividual or is otherwise corrupt, please return INDIVIDUAL or CORRUPT to mark these samples.",
    }

    max_tokens = 30

    @classmethod
    def preprocess_name(cls, name: str) -> str:

        prompt = {"role": "user", "content": f"{name}"}

        response = openai.ChatCompletion.create(
            model=cls.model,
            messages=[cls.system_prompt, prompt],
            max_tokens=cls.max_tokens,
        )

        return response["choices"][0]["message"]["content"].strip()


class SimpleGMBHRemover:
    patterns_to_remove = [
        r"gmbh",
        r"gbr",
        r"mbh",
        r"kg",
        r"k\.g\.",
        r"aktiengesellschaft",
        r"arbeitsgemeinschaft",
        r"g\.m\.b\.h\.",
        r"ag",
        r"a\.g\.",
        r"kommanditgesellschaft",
        r"auf aktien",
        r"gmbh\.",
        r"gbr\.",
        r"mbh\.",
        r"\& co\.",
        r"kg\.",
        r"aktiengesellschaft\.",
        r"arbeitsgemeinschaft\.",
        r"g\.m\.b\.h\..",
        r"ag\.",
        r"kommanditgesellschaft\.",
        r"auf aktien\.",
        r"ug",
        r"haftungsbeschränkt",
        r"\(",
        r"\)",
        r"\&",
        r"co",
        r"e\.v\.",
        r";",
    ]

    @classmethod
    def preprocess_name(cls, name: str) -> str:
        name = name.lower()
        for pattern in cls.patterns_to_remove:
            name = re.sub(
                r"\s+", " ", name
            )  # Replace multiple spaces with a single space
            name = re.sub(r"\s,\s", ", ", name)
            name = re.sub(r"\b" + pattern + r"(?=\b|\s|\.|,|$)", "", name)
        return name.strip()


def clean_company_names(names: List[str], output_file: str):
    n_names = len(names)
    with open(output_file, "w") as file:
        file.write("Original Name; Clean Name\n")
        for i, name in enumerate(names):
            clean_name = SimpleGMBHRemover.preprocess_name(name)
            file.write(f"{name.replace(';', '')}; {clean_name.replace(';', '')}")


if __name__ == "__main__":
    pass
