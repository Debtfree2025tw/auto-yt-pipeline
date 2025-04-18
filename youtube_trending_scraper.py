import os
import pickle
import google.auth
from whisper_gpt_analyzer import analyze_video
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import webbrowser  # To open the authorization URL

# Define the API scope
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Authenticate and build the YouTube API client
def youtube_authenticate():
    creds = None
    # Load existing credentials if available
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/taijunwaters/Documents/Youtube Scrapper/client_secret.json', SCOPES
            )
            auth_url, _ = flow.authorization_url(
                access_type='offline', include_granted_scopes='true'
            )
            print(f"Please visit this URL to authorize this application: {auth_url}")
            webbrowser.open(auth_url, new=2)
            creds = flow.run_local_server(port=8080)
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

# Main function to search and analyze videos
def main():
    youtube = youtube_authenticate()
    # List of search queries
    queries = [
        "AI agents",
        "n8n automation workflows",
        "ElevenLabs voice cloning",
        "AI voice assistants",
        "ai business ideas",
        "best business ideas for 2025",
        "deepseek"
    ]

    for query in queries:
        print(f"\n🔍 Searching for: {query}")
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=21
        )
        try:
            response = request.execute()
            for item in response.get('items', []):
                title = item['snippet']['title']
                vid = item['id']['videoId']
                url = f"https://www.youtube.com/watch?v={vid}"
                print(f"Title: {title}")
                print(f"URL:   {url}")
                print('---')
                # Send URL to the analyzer
                analyze_video(url)
        except HttpError as error:
            print(f"An error occurred while searching '{query}': {error}")

if __name__ == '__main__':
    main()
