import pickle as pkl
import os
from pytubefix import YouTube
import concurrent.futures

VIDEO_SAVE_DIRECTORY = "./videos"
AUDIO_SAVE_DIRECTORY = "./audio"

def read_pkl_array():
    with open("map.pkl", "rb") as arr_pkl:
        ids = pkl.load(arr_pkl)
    return ids

def create_directories():
    for dir in [VIDEO_SAVE_DIRECTORY, AUDIO_SAVE_DIRECTORY]:
        if not os.path.exists(dir):
            os.mkdir(dir, mode=777)


# Function to download audio for a single video
def download_audio(id):
    video_url = f'https://www.youtube.com/watch?v={id}'
    video = YouTube(video_url)
    try:
        if f'{video.title}.mp3' in audio_filename_list:
            return f"already downloaded {id}"
        audio = video.streams.first()
        audio.download(AUDIO_SAVE_DIRECTORY, filename=f'{video.title}.mp3', timeout=30, max_retries=2)
        return f"Downloaded audio for video {id}"
    except Exception as e:
        try:
            print(f'#{id} - {video.title}')
        except:
            pass
        import traceback
        return f"Failed to download audio for video {id} {traceback.format_exc()}"

def get_videos_parallel(ids):
    global audio_filename_list
    audio_filename_list = os.listdir(AUDIO_SAVE_DIRECTORY)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(download_audio, ids))
    
    for result in results:
        print(result)

def main():
    create_directories()
    ids = read_pkl_array()
    print(len(ids))
    get_videos_parallel(ids)
    

if __name__ == "__main__":
    main()