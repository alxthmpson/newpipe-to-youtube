# NewPipe to YouTube

A Python script to bulk subscribe to YouTube channels using the YouTube Data API v3 based on your NewPipe subscriptions.

## Features
- **Bulk subscribe** to channels from NewPipe subscriptions JSON file
- **Handles existing subscriptions** (skips duplicates)

## Prerequisites
- Python 3.6+
- Google API project with YouTube Data API v3 enabled
- `client_secrets.json` from Google Cloud Console

## Setup

1. **Enable YouTube Data API**
   - Create a project at [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "YouTube Data API v3"
   - Create OAuth 2.0 credentials (Desktop app type)
   - Download credentials as `client_secrets.json`

2. **Install dependencies**
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
## Usage

- Clone repo or just download `newpipe-to-youtube.py`
- Export subscriptions from NewPipe - `subscriptions.json`
- Place `newpipe-to-youtube.py`, `client_secrets.json` and `subscriptions.json` in the same folder
- Run the script
    ```bash
    python newpipe-to-youtube.py
    ```
- Authenticate when prompted:

    1. Browser will open for Google sign-in
    2. Grant "Manage YouTube subscriptions" permission
