import requests


# Функция получения нужных котировок
def get_btc():
    url_rub_eur = 'https://api.fixer.io/latest'
    url_rub_usd = 'https://api.fixer.io/latest?base=USD'
    response_rub_eur = requests.get(url_rub_eur).json()
    response_rub_usd = requests.get(url_rub_usd).json()
    ruble_eur = response_rub_eur['rates']['RUB']
    ruble_usd = response_rub_usd['rates']['RUB']
    a = str('1 доллар = ' + str(ruble_usd) + ' рублей ')
    b = str('1 евро = ' + str(ruble_eur) + ' рублей, ')
    c = a + b
    return c


def main():
    print(get_btc())

if __name__ == '__main__':
    main()
