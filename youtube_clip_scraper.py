import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API key
API_KEY = "AIzaSyACXtbqX1j84PinTcgobJMfv33WynPlktQ"  # Store the API key in .env for security

# Set up the YouTube API client
youtube = build('youtube', 'v3', developerKey="AIzaSyACXtbqX1j84PinTcgobJMfv33WynPlktQ")

# Function to get video details by video ID
def get_video_details(video_id):
    try:
        # Request video details from YouTube API
        request = youtube.videos().list(
            part='snippet,statistics',  # 'snippet' gives details like title, description
            id=video_id
        )
        response = request.execute()

        if 'items' in response:
            video = response['items'][0]  # Get first item in response (should be 1 item)
            title = video['snippet']['title']
            description = video['snippet']['description']
            view_count = video['statistics']['viewCount']
            
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"Views: {view_count}")
        else:
            print(f"No video found with ID: {video_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    video_id = input("Enter YouTube video ID: ")
    get_video_details(video_id)
