from langchain_aws.chat_models.bedrock import ChatBedrockConverse




llm = ChatBedrockConverse(
    credentials_profile_name="bedrock-admin",
    model="mistral.mistral-large-2407-v1:0",
    temperature=0.5,
    max_tokens=8000,
    region_name='us-west-2'

)   

if __name__ == "__main__":
    print(llm.invoke("What is the capital of France?"))