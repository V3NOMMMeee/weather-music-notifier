import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()

# Credentials and configuration
weather_api_key = os.getenv('WEATHER_API_KEY')
city = 'London'
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_sandbox_number = os.getenv('TWILIO_WHATSAPP_SANDBOX_NUMBER')
whatsapp_recipient_number = os.getenv('WHATSAPP_RECIPIENT_NUMBER')
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Fetch weather data
weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
weather_data = requests.get(weather_url).json()
weather_description = weather_data['weather'][0]['description']

# Get Spotify access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={'grant_type': 'client_credentials'},
    headers={
        'Authorization': 'Basic ' + base64.b64encode(f'{spotify_client_id}:{spotify_client_secret}'.encode()).decode()
    }
)
if auth_response.status_code == 200:
    access_token = auth_response.json().get('access_token')
else:
    print('Failed to get Spotify access token:', auth_response.json())
    access_token = None

if access_token:
    # Get music recommendation
    headers = {'Authorization': f'Bearer {access_token}'}
    recommendation_url = 'https://api.spotify.com/v1/recommendations'
    params = {'seed_genres': 'pop', 'limit': 1}
    song_response = requests.get(recommendation_url, headers=headers, params=params)

    if song_response.status_code == 200:
        song_data = song_response.json()
        if song_data['tracks']:
            song_name = song_data['tracks'][0]['name']
            song_artist = song_data['tracks'][0]['artists'][0]['name']

            # Send WhatsApp message
            client = Client(twilio_account_sid, twilio_auth_token)
            message = client.messages.create(
                body=f"The weather in {city} is currently {weather_description}. Here is a song for you: {song_name} by {song_artist}",
                from_=whatsapp_sandbox_number,
                to=whatsapp_recipient_number
            )
            print(f"Message sent with SID: {message.sid}")
        else:
            print('No tracks found in the Spotify recommendation response.')
    else:
        print('Failed to get song recommendation:', song_response.json())
else:
    print('Cannot proceed without Spotify access token.')
