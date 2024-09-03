# yt-down

Allow to download files from a youtube playlist. Just run the `get_data.py` to extract playlist data and the `downloader.py` to download from the data extracted.

You can make files itunes proof with `ffmpeg`:

```shell
for f in *.mp3; do ffmpeg -i "$f" -vn -c:a copy "audio_low/$("$f")"; done
```

### Authentification:

Create a `secret.json` at the root of the project ([doc here](https://stackoverflow.com/questions/65816603/how-to-generate-client-secret-json-for-google-api-with-offline-access))

```json
{
  "api_key": "XXX",
  "installed": {
    "key": "XXX",
    "client_id": "XXX",
    "project_id": "XXX",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "XXX",
    "redirect_uris": ["http://localhost"]
  }
}
```

nomook