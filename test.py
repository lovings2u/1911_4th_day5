from bs4 import BeautifulSoup
import requests

def lotto():
    url = 'https://dhlottery.co.kr/gameResult.do?method=byWin'
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    numbers = html.select('div.win span')
    lotto = []
    for number in numbers:
        print(number.text)
        lotto.append(number)

lotto()