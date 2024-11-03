# app.py
import gradio as gr
from crew_workflow import YTCrew

crew_workflow= YTCrew()

def summarize_video(video_url):
    result = crew_workflow.crew().kickoff(inputs={'video_url': video_url})
    return result

iface = gr.Interface(
    fn=summarize_video,
    inputs=gr.Textbox(label="YouTube Video URL"),
    outputs="text",
    title="YouTube Video Summarizer"
)

if __name__ == "__main__":
    iface.launch()
