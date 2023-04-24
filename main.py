import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

def get_element(soup_elem):
    return soup_elem.find('span', {'class': 'prdname'}).text.split('@')[0].strip().replace('-', ' '), \
           soup_elem.find('span', {'class': 'count'}).text.replace(',', '').strip()


def get_cpus_cpubenchmark():
    cpu_link = 'https://www.cpubenchmark.net/high_end_cpus.html'
    resp = requests.get(cpu_link)
    soup = BeautifulSoup(resp.text, 'lxml')
    elements = {}
    for elem in soup.find('ul', {'class': 'chartlist'}).findAll('a'):
        name, bench = get_element(elem)
        elements[name] = bench
    return elements


def print_cpus_hardprice():

    with open('hardprice_cpu.html', 'r', encoding='utf-8') as f:
        hardprice_text = f.read()
    soup = BeautifulSoup(hardprice_text, 'lxml')
    cpu_elements = get_cpus_cpubenchmark()

    names = []
    benchs = []
    prices = []
    shops = []

    for elem in soup.findAll('div', {'class': 'products-list-v2__item'}):
        cpu_name = (elem.find('a', {'class': 'title'}).text.strip().replace('-', '').replace('  ', ' '))

        min_price = 100000000
        min_shop = 'Unknown'
        for elem2 in elem.find('div', {'class': 'products-list-v2__item-prices'}):
            if elem2.text.strip() != '':
                name = elem2.find('span').text
                price = elem2.find('b', {'class': 'price'}).text.replace(' ', '').replace('p.', '').strip()
                if price != 'ожидается':# and name != 'CU':
                    if int(price) < min_price:
                        min_shop = name
                        min_price = int(price)

        bench = 1
        for elem in cpu_elements:
            if cpu_name.lower().find(elem.lower()) != -1:
                bench = int(cpu_elements[elem])
        if bench > 1:
            print('{0} has benchmark = {1} with price = {2} in shop {3}'.format(cpu_name, bench, min_price, min_shop))
        names.append(cpu_name)
        benchs.append(bench)
        prices.append(min_price)
        shops.append(min_shop)
    df = DataFrame({'CPU': names, 'BENCH': benchs, 'PRICE': prices, 'SHOP': shops})
    df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


if __name__ == '__main__':
    print_cpus_hardprice()
