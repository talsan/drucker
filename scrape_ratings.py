from lxml import html
import requests
import time
import json
import os

OUTPUT_DIR = './data'


def str_to_int(k, v):
    if k not in ['COMPANY', 'YEAR']:
        v = float(v)
    return v


for yyyy in range(2017, 2023):
    print(f'processing: {yyyy}')
    r = requests.get(f'https://www.drucker.institute/{yyyy}-drucker-institute-company-ranking/')
    root = html.fromstring(r.content)

    if yyyy <= 2018:
        headers = root.xpath('//table[@class="waffle"]/thead/tr/th/text()')
        rows = root.xpath('//table[@class="waffle"]/tbody/tr')
    else:
        headers = root.xpath('//div[@class="Table-ranking"]/table/thead/tr/th/text()')
        rows = root.xpath('//div[@class="Table-ranking"]/table/tbody/tr')

    output = []
    for row in rows:
        row_elements = row.xpath('./td')
        row_values = [' '.join(element.xpath('.//text()')) for element in row_elements]
        if len(row_values) == len(headers):
            row_data_raw = dict(zip(['YEAR'] + headers, [yyyy] + row_values))
            row_data = {k: str_to_int(k, v) for k, v in row_data_raw.items()}
            output.append(row_data)
        else:
            raise Exception(f'issue parsing drucker ratings table elements:\n'
                            f'headers: {headers}\n'
                            f'row entries: {row_values}')

    with open(os.path.join(OUTPUT_DIR, f'drucker_ratings_{yyyy}.json'), 'w') as f:
        json.dump(output, f, indent=2)

    time.sleep(2)
