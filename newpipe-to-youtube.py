import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# API configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    """Authenticate and return the YouTube API service"""
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

def process_subscriptions(service):
    """Process subscriptions from JSON file with nested structure"""
    try:
        with open('subscriptions.json', 'r') as file:
            data = json.load(file)
            subscriptions = data.get('subscriptions', [])
            
            if not subscriptions:
                print("No subscriptions found in the file.")
                return
            
            for channel_obj in subscriptions:
                url = channel_obj.get('url')
                name = channel_obj.get('name', 'Unknown Channel')
                
                if not url:
                    print(f"Skipping entry with missing URL: {name}")
                    continue
                
                # Extract channel ID from URL
                if '/channel/' in url:
                    channel_id = url.split('/channel/')[-1].split('/')[0]
                else:
                    print(f"Skipping invalid URL for {name}: {url}")
                    continue
                
                # Create subscription request
                body = {
                    'snippet': {
                        'resourceId': {
                            'kind': 'youtube#channel',
                            'channelId': channel_id
                        }
                    }
                }
                
                try:
                    response = service.subscriptions().insert(
                        part='snippet',
                        body=body
                    ).execute()
                    print(f"Subscribed to {name} ({response['snippet']['title']})")
                except HttpError as e:
                    if e.resp.status == 400 and 'already exists' in str(e):
                        print(f"Already subscribed to {name} ({channel_id})")
                    else:
                        print(f"Error subscribing to {name}: {str(e)}")
    
    except FileNotFoundError:
        print("subscriptions.json file not found!")
    except json.JSONDecodeError:
        print("Invalid JSON format in subscriptions.json")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    youtube = get_authenticated_service()
    process_subscriptions(youtube)