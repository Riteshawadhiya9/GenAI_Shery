from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

# model = init_chat_model("google_genai:gemini-2.5-flash")
model = init_chat_model("groq:openai/gpt-oss-120b")

# print(model)


# response = model.invoke("What is the difference among AI and Agentic AI and AI Agents? Explain in detail with examples.In hinglish. and what's the current time -> Bhopal,India")

response = model.invoke("tell what is Lnagchain and Langgraph in detail with examples and use cases. and also tell about the future of langchain and langgraph in the next 5 years. IN Simple English with exaples")

print(response.content)