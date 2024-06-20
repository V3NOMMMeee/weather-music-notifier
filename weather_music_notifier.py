import requests
from twilio.rest import Client

# Credentials and configuration
weather_api_key = '38d5939a09c3163059825c74843b4132'
city = 'Ghaziabad'
twilio_account_sid = 'AC0f0dc35b367ac81165494f681a9c260b'
twilio_auth_token = '9b79e2f4c12b53eb66ec781489e48df8'
whatsapp_sandbox_number = 'whatsapp:+13479675562'
whatsapp_recipient_number = 'whatsapp:+917042581350'
spotify_client_id = 'f379600651be464db610ea2ac90e9245'
spotify_client_secret = '72034ec2b8f540908b819b9240e8b7cb'

# Fetch weather data
weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
weather_data = requests.get(weather_url).json()
weather_description = weather_data['weather'][0]['description']

# Get Spotify access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={'grant_type': 'client_credentials'},
    headers={'Authorization': f'Basic {spotify_client_id}:{spotify_client_secret}'}
)
access_token = auth_response.json()['access_token']

# Get music recommendation
headers = {'Authorization': f'Bearer {access_token}'}
recommendation_url = 'https://api.spotify.com/v1/recommendations'
params = {'seed_genres': 'pop', 'limit': 1}
song_data = requests.get(recommendation_url, headers=headers, params=params).json()
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
