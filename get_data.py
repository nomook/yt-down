# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import json
import pickle
import sys

import googleapiclient.discovery
import googleapiclient.errors

CLIENT_SECRETS_FILE = "secrets.json"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_playlist_infos(youtube, playlist_id):
    request = youtube.playlists().list(
                part="contentDetails",
                id=playlist_id
            )
    return request.execute()
    

def get_page_playlist(youtube, playlist_id, token = None):
    if token:
        request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=token
            )
    else:
        request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50
            )
    response = request.execute()
    next_token = response.get('nextPageToken')
    return response, next_token

def main(playlist_id='PLLc45M6lei1u10UDGL5yrGUuDn5OoT46n'):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    
    with open(CLIENT_SECRETS_FILE, "r+") as f:
        secret_data = json.load(f)
    youtube = googleapiclient.discovery.build(
               api_service_name, 
               api_version, 
               developerKey=secret_data.get('api_key'))
    playlist_infos = get_playlist_infos(youtube=youtube, playlist_id=playlist_id)
    items_count = playlist_infos.get("contentDetails", {}).get('itemCount', 0)

    result = [None] * items_count
    
    response, next_token = get_page_playlist(youtube=youtube, playlist_id=playlist_id)
    for vid in response['items']:
        result.append(vid.get('contentDetails', {}).get('videoId', 'ERROR'))

    cursor = 50
    while next_token:
        response, next_token = get_page_playlist(youtube=youtube, playlist_id=playlist_id, token=next_token)

        for vid in response['items']:
            result.append(vid.get('contentDetails', {}).get('videoId', 'ERROR'))
        cursor += 50
    with open('map.pkl', 'wb') as f:
        pickle.dump(result, f)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
        exit(0)
    main()