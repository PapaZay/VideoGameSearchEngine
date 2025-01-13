import requests
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_access_token():
    twitch_url = "https://id.twitch.tv/oauth2/token"

    params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
    }

    response = requests.post(twitch_url, params=params)

    if response.status_code == 200:
        data = response.json()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in")
        token_type = data.get("token_type")

        #print(f"Access Token: {access_token}")
        #print(f"Expires In: {expires_in} seconds")
        #print(f"Token Type: {token_type}")
        return access_token
    else:
        print(f"Error: {response.status_code} Unable to retrieve token")
        print(response.text)
        return None

def get_games(query):
    access_token = get_access_token()
    if not access_token:
        return {"error": "Can't proceed without access token"}
         
    
    IDGB_url = "https://api.igdb.com/v4/games"
    IDGB_company_endpoint = "https://api.igdb.com/v4/companies"

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}"
    }
    name = "The Last of Us"
    dev = "Naughty Dog"
    body = f'search "{name}"; fields name; limit 50;'
    body2 = f'where name = "{dev}"; fields name;'
    body3 = f'search "{query}"; fields name, summary, first_release_date; limit 10;'

    response = requests.post(IDGB_url, headers=headers, data=body3)
    #response2 = requests.post(IDGB_company_endpoint, headers=headers, data=body2)

    if response.status_code == 200:
        data = response.json()
        return data
        for game in data:
           """game_name = game.get('name', 'Unknown Name')
           #companies = game.get('involved_companies', 'No Companies Info')
           print(f"Name: {game_name}")"""
    else:
        print(f"Error {response.status_code}: Unable to fetch games")
        print(response.text)
    
    """if response2.status_code == 200:
        data2 = response2.json()
        for company in data2:
            company_name = company.get('name', 'Unknown Developer')
            print(f"Developer: {company_name}")
    else:
        print(f"Error {response2.status_code}: Unable to fetch developers")
        print(response2.text)"""


#get_access_token()
#get_games("Mario")