import cianparser
import csv
import time
import random

def save_to_csv(flats_data, filename="flats_data.csv", mode='a'):
    if mode == 'a':
        keys = flats_data[0].keys()
        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(flats_data)
    else:
        with open(filename, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=flats_data[0].keys())
            writer.writerows(flats_data)

def fetch_data_with_retries(parser, page, retries=3):
    for attempt in range(retries):
        try:
            data = parser.get_flats(deal_type="sale", rooms=(1, 2), additional_settings={"start_page": page, "end_page": page})
            return data
        except Exception as e:
            print(f"Ошибка при запросе страницы {page}: {e}. Попытка {attempt + 1} из {retries}")
            time.sleep(random.uniform(8, 16))
    return []
moscow_parser = cianparser.CianParser(location="Егорьевск")
all_flats = []
total_flats = 0
max_flats = 100000 
output_file = "kv_db.csv"
with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
    pass
for page in range(1, 1000):
    data = fetch_data_with_retries(moscow_parser, page)
    if not data:
        break 
    all_flats.extend(data)
    total_flats += len(data)
    save_to_csv(data, filename=output_file, mode='a')   
    time.sleep(random.uniform(3, 6))
    if total_flats >= max_flats:
        break

