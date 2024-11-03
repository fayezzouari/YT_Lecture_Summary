from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.youtube_summarizer_tool import youtube_summarizer_tool
# from .model_aws import llm
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

llm = ChatGroq(
    model="groq/llama-3.2-90b-vision-preview",

    temperature=0,
    max_tokens=8000,       # Add explicit max_tokens as an integer
    timeout=30,            # Set a reasonable timeout
    max_retries=2,
)


agent_emojis = {
    "Analysis Agent": "🔍",
    "Feedback Agent": "📝",
}

@CrewBase
class YTCrew:
    """YT crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    

    @agent
    def video_scraping_agent(self) -> Agent:
        return Agent(
            role="Video Scraping Agent",
            goal="Scrape Youtube link and return the content and information from {video_url}.",
            verbose=True,
            llm=llm,
            max_iter=2,
            allow_delegation=False,
        
            backstory=(
                "You are a specialist in scraping data from the web. You have a keen eye for detail and can extract the essence"
                "of web pages effectively. You are tasked with scraping data from a YouTube video link and extracting key data points from the specified video using a youtube_summarization_tool which is going to provide you with transripts of the video which you have to use to identify the main ideas."
            ),
            # step_callback=create_streamlit_callback('Biogas Data Scraping Agent', agent_emojis['Scraping Agent'])
        )

    @agent
    def video_summarization_agent(self) -> Agent:
        return Agent(
            role="Video Summarization Agent",
            goal="Summarize key points from YouTube video content, focusing on major details.",
            verbose=True,
            llm=llm,
            max_iter=2,
            allow_delegation=False,
        
            backstory=(
                "You are a specialist in analyzing spoken content and condensing it into"
                "important highlights. You have a keen eye for detail and can extract the essence"
                "lectures, speeches, and presentations effectively."
                "Try to summarize the content that you get from the scraping agent."
            ),
            # step_callback=create_streamlit_callback('Biogas Data Analysis Agent', agent_emojis['Analysis Agent'])
        )

    @task
    def scrape_video(self) -> Task:
        return Task(
            description="Given a YouTube video link, scrape the video to summarize a lecture and get the main ideas.",
            expected_output="A list of key data points extracted from the video.",
            agent=self.video_scraping_agent(),
            tools=[youtube_summarizer_tool],
        )

    @task
    def summarize_video(self) -> Task:
        return Task(
            description="Given a YouTube video link, extract the transcript and summarize it"
            "concisely, focusing on the most critical points of the lecture."
            "Use a maximum of three concise paragraphs.",
            expected_output="    A detailed summary that captures the main ideas of the video.",
            context={self.scrape_video()},
            agent=self.video_summarization_agent(),
        )

 

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.video_scraping_agent(),
                self.video_summarization_agent(),        
            ],
            tasks=[
                self.scrape_video(),
                self.summarize_video(),
            ],
            process=Process.sequential,
            full_output=True,   
            verbose=1,
        )