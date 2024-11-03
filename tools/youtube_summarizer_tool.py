# src/youtube_summarizer/tools/youtube_summarizer_tool.py
from crewai_tools import tool
import requests
import re
from .basic_scraping import get_subtitles
from .chunk_trans import summarize_text

@tool
def youtube_summarizer_tool(video_url: str) -> str:
    """ Summarize the content of a YouTube video based on its transcript. """
    # Extract transcript from YouTube (simplified example; adjust based on API/library)
    transcript = fetch_youtube_transcript(video_url)
    return transcript

def fetch_youtube_transcript(video_url):
    """ Placeholder function to fetch transcript from YouTube video. """
    # Placeholder function - replace with actual transcript extraction logic
    video_id = re.search(r'v=([A-Za-z0-9_-]+)', video_url).group(1)
    print("video id: ",video_id)
    res=summarize_text(get_subtitles(video_id))
    return res

