import csv 
import json
import logging
import pandas as pd


def convert_txt_to_csv(txt_file: str, csv_path: str):
    try:
        data = []
        with open(txt_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            headline, link, label = line.strip().split("|")
            data.append({"Headline": headline, "Link": link, "Label": label})

        # convert to DataFrame
        df = pd.DataFrame(data)

        # save DataFrame to file .csv
        df.to_csv(csv_path, index=False, encoding="utf-8")

    except Exception as e:
        logging.error(f"Error occurred while converting txt to csv.")


def convet_csv_to_json(csv_path, json_path):
    try: 
        csv_file = open(csv_path, 'r', encoding= 'utf-8')
        json_file = open(json_path, 'r', encoding= "utf-8")

        reader = csv.DictReader(csv_file)
        for row in reader:
            json.dump(row, json_file)
            json_file.write('\n')
    except Exception as e: 
        logging.error(f"Error occurred while converting CSV to JSON.")
