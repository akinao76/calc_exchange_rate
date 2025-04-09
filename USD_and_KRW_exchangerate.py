import os
from dotenv import load_dotenv #API 하드 코딩 방지 -> .env 파일 사용
import requests
import json

#기준 통화 선택
def choice_base_currency():
    base_currency_options = ["USD", "KRW"]
    while True:
        base_currency = input("기준 통화를 선택해 주세요 (USD, KRW 중 택 1) : ").upper()
        if base_currency in base_currency_options:
            print(f'기준 통화가 "{base_currency}"로 설정되었습니다.')
            return base_currency
        print("잘못 입력하셨습니다. 다시 입력해주세요.")

#환전 가능한 국가 선택
def choice_exchange_country():
    exchange_country = {
        "US": "USD",
        "KOREA": "KRW",
        "EU": "EUR",
        "JAPAN": "JPY",
        "UK": "GBP",
        "CHINA": "CNY",
        "CANADA": "CAD",
        "AUSTRALIA": "AUD",
        "SWISS": "CHF",
        "INDIA": "INR",
        "SINGAPORE": "SGD"
    }

#환전 가능한 국가 목록 출력
    print("환전 가능한 국가 목록입니다:")
    for key in exchange_country.keys():
        print(key)

    while True:
        select_country = input("국가를 입력하세요 : ").upper()
        if select_country in exchange_country:
            print(f"{select_country}로 환전을 진행합니다.")
            return exchange_country[select_country]
        print("잘못 입력하셨습니다. 다시 입력해주세요.")

#환율 계산
def exchange_rate_calculator(base_currency, exchange_country):
    #API 키 불러오기
    load_dotenv()
    API_Key = os.getenv("API_KEY")
    if not API_Key: #API 키가 설정되지 않았을 때 오류 발생
        raise ValueError("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    url = f"https://openexchangerates.org/api/latest.json?app_id={API_Key}"
    response = requests.get(url)
    data = json.loads(response.text)

    exchange_rate = data["rates"].get(exchange_country)
    if exchange_rate is None:
        print("환율 정보를 가져오는 데 실패했습니다.")
        return None

    while True:
        try:
            exchange_amount = float(input("환전할 금액을 입력하세요 : "))
            if exchange_amount < 0:
                print("금액은 0 이상이어야 합니다. 다시 입력해주세요.")
            else:
                break
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력해주세요.")

    if base_currency == "USD": #base_currency == "USD"
        calc_amount = exchange_amount * exchange_rate
    else:  # base_currency == "KRW"
        krw_exchange_rate = data["rates"].get("KRW")
        if krw_exchange_rate is None:
            print("KRW 환율 정보를 가져오는 데 실패했습니다.")
            return None
        calc_amount = (exchange_amount / krw_exchange_rate) * exchange_rate

    print(f"환전 금액은 {calc_amount:.2f} {exchange_country}입니다.")
    return calc_amount

if __name__ == "__main__":
# 실행 부분
    set_base_currency = choice_base_currency()
    set_exchange_country = choice_exchange_country()
    calc_amount = exchange_rate_calculator(set_base_currency, set_exchange_country)

#calc_amount가 정상일때만 출력
    if calc_amount is not None:
        print(f"최종 환전 금액: {calc_amount:.2f} {set_exchange_country}")
