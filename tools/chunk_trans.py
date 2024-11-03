from langchain_groq import ChatGroq
import time


def split_text_into_chunks(text, chunk_size=450):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

llm = ChatGroq(
    model="llama-3.2-90b-vision-preview",
    api_key="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",
    temperature=0.5,
    max_tokens=8000,  # Limit the response length to avoid rate limit errors
    timeout=30,
    max_retries=2,
)

def summarize_text(text):
    summaries = []
    for chunk in split_text_into_chunks(text, chunk_size=450):  # Adjust `chunk_size` if needed
        prompt = f"Summarize the following text into a single paragraph:\n\n{chunk}"
        try:
            response = llm.invoke(prompt)  # Make the API call to summarize the chunk
            summaries.append(response.content)
            print("chunk id", len(summaries) )
        except Exception as e:
            print(f"An error occurred: {e}")

    # Combine all chunk summaries into a final summary
    final_summary = " ".join(summaries)
    print("Final Summary:\n", final_summary)
    return final_summary


if __name__ == "__main__":  
    text= str(input("Enter the text you want to summarize: "))
    summarize_text(text)

