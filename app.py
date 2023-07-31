import requests
import json
import pandas as pd

def get_refresh_token():
    url = "https://api.jquants.com/v1/token/auth_user"

    payload = json.dumps({
        "mailaddress": "naoyanickf@gmail.com",
        "password": "Fujisyan0731"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["refreshToken"]

def get_id_token(refresh_token):
    url = f'https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}'

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["idToken"]

def get_breakdown(id_token, code, from_date, to_date):
    url = f'https://api.jquants.com/v1/markets/breakdown?from={from_date}&to={to_date}&code={code}'
    payload = {}
    headers = {
        'Authorization': f'Bearer {id_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['breakdown']

def get_daily_quotes(id_token, code, from_date, to_date):
    url = f'https://api.jquants.com/v1/prices/daily_quotes?from={from_date}&to={to_date}&code={code}'
    payload = {}
    headers = {
        'Authorization': f'Bearer {id_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['daily_quotes']

if __name__ == "__main__":
    refresh_token = get_refresh_token()
    id_token = get_id_token(refresh_token)
    code = "8411"
    from_date = "2022-01-01"
    to_date = "2023-06-30"
    breakdown = get_breakdown(id_token, code, from_date, to_date)
    breakdown_df = pd.DataFrame(breakdown)

    daily_quotes = get_daily_quotes(id_token, code, from_date, to_date)
    daily_quotes_df = pd.DataFrame(daily_quotes)
    daily_quotes_df = daily_quotes_df.drop('Code', axis=1)

    df = pd.merge(breakdown_df, daily_quotes_df, on='Date')

    df['OpenCloseReturn'] = df['AdjustmentClose'] - df['AdjustmentOpen']
    df['OpenCloseReturnRatio'] = ((df['AdjustmentClose'] - df['AdjustmentOpen']) / df['AdjustmentOpen']) * 100

    # merged_dfをcsvに出力
    df.to_csv('merged_df.csv', index=False)

