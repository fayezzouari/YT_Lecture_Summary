# Install youtube-transcript-api if you haven't already
# pip install youtube-transcript-api

from youtube_transcript_api import YouTubeTranscriptApi
import re
# Function to get subtitles
def get_subtitles(video_id, language='en'):
    res=""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        for line in transcript:
           
            res+=line["text"]+ " "
        return res
    except Exception as e:
        print(f"Could not retrieve subtitles: {e}")

# Replace 'your_video_id_here' with the actual YouTube video ID

if __name__ == "__main__":
    data=get_subtitles("9vM4p9NN0Ts")
    print(data)