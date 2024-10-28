# 2 ветка странно себя ведет будем тут тестить чтото делать смотреть и короче все воэ это вот
import cianparser
import csv
import time
import random

def save_to_csv(flats_data, filename="zxc.csv"):
    keys = flats_data[0].keys()
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writerows(flats_data)

def fetch_flats(parser, page):
    try:
        data = parser.get_flats(deal_type="sale", rooms=(1), additional_settings={"start_page": page, "end_page": page})
        for flat in data:
            flat.pop('url', None)
            flat.pop('author', None)
            flat.pop('author_type', None)
            

            metro_info = flat.get('metro', [{}])[0]
            flat['nearest_metro'] = metro_info.get('name', 'Нет информации')
            flat['time_to_metro'] = metro_info.get('time', 'Не указано')
            flat['total_floors'] = flat.get('total_floors', 'Не указано')
            flat['floor'] = flat.get('floor', 'Не указано')
            flat['square'] = flat.get('square', 'Не указано')
            flat['kitchen_square'] = flat.get('kitchen_square', 'Не указано')
            flat['price'] = flat.get('price', 'Не указано')
            
        return data
    except Exception as e:
        print(f"Ошибка на странице {page}: {e}")
        return []

parser = cianparser.CianParser(location="Долгопрудный")

for page in range(1, 1000):
    flats = fetch_flats(parser, page)
    if not flats:
        break
    save_to_csv(flats)
    time.sleep(random.uniform(3, 6))

print("Парсинг завершён.")