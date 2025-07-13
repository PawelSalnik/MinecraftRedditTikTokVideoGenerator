# Minecraft Reddit TikTok Video Generator

This Python script automatically generates TikTok-style vertical videos by combining Minecraft gameplay footage with random Reddit posts converted to speech. It downloads a random post from the **r/todayilearned** subreddit, converts the post text to audio, and then merges it with a Minecraft video clip, creating a short vertical video ready for sharing.

## Features

- Fetches a random hot post (title + selftext) from the "todayilearned" subreddit using Reddit API.
- Converts the post text to speech using Google Text-to-Speech (gTTS).
- Automatically crops Minecraft videos to vertical 9:16 aspect ratio suitable for TikTok.
- Merges generated audio with video and outputs a video file.
- Saves generated videos in a separate folder with incremental filenames.
- Runs interactively in a loop to generate multiple videos.
