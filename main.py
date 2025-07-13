import os
import random
from gtts import gTTS
import praw
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. PATHS
VIDEO_INPUT_FOLDER = "./videos"            # Folder with .mp4 files (Minecraft)
VIDEO_OUTPUT_FOLDER = "./generated_videos" # Folder for generated TikToks

# Ensure the output folder exists
os.makedirs(VIDEO_OUTPUT_FOLDER, exist_ok=True)

# 2. REDDIT API - YOUR CREDENTIALS
reddit = praw.Reddit(
    client_id="bO5GSDnnUWGMGkpvKpofSA",
    client_secret="1kO-T5-3f-LeRz9FXLKOtafBCrKIvw",
    user_agent="KSLordBot/0.1"
)

# 3. GET RANDOM POST (full: title + selftext)
def get_full_reddit_post():
    subreddit = reddit.subreddit("todayilearned")
    posts = list(subreddit.hot(limit=50))
    post = random.choice(posts)
    full_text = post.title
    if post.selftext:
        full_text += ". " + post.selftext
    return full_text

# 4. FIND FIRST MP4 FILE
def get_first_mp4(folder):
    for file in os.listdir(folder):
        if file.endswith(".mp4"):
            return os.path.join(folder, file)
    return None

# 5. CREATE AUDIO FROM TEXT
def text_to_speech(text, filename="audio.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# 6. FIND NEXT FREE VIDEO FILE NAME
def get_next_video_filename(folder):
    existing = [f for f in os.listdir(folder) if f.startswith("generated_video_") and f.endswith(".mp4")]
    numbers = []
    for f in existing:
        try:
            num = int(f.replace("generated_video_", "").replace(".mp4", ""))
            numbers.append(num)
        except ValueError:
            continue
    next_num = max(numbers) + 1 if numbers else 1
    return os.path.join(folder, f"generated_video_{next_num}.mp4")

# 7. VIDEO EDITING
def make_tiktok_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)

    # Crop video to vertical 9:16 aspect ratio
    w, h = video.size
    new_w = int(h * 9 / 16)
    if new_w > w:
        new_w = w

    x_center = w // 2
    x1 = x_center - new_w // 2
    x2 = x_center + new_w // 2

    video = video.crop(x1=x1, x2=x2)

    audio = AudioFileClip(audio_path)

    # Cut video length to audio length and set audio
    final = video.set_audio(audio).subclip(0, audio.duration)

    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    while True:
        video_file = get_first_mp4(VIDEO_INPUT_FOLDER)
        if not video_file:
            print("Error: No .mp4 file found in folder:", VIDEO_INPUT_FOLDER)
            exit()

        text = get_full_reddit_post()
        print(f"Full Reddit post:\n{text}")

        audio_file = text_to_speech(text)

        output_file = get_next_video_filename(VIDEO_OUTPUT_FOLDER)
        make_tiktok_video(video_file, audio_file, output_file)

        print(f"Done! Saved to: {output_file}")

        loop = input("Do you want to create another video? (y/n): ").strip().lower()
        if loop != 'y':
            break
