from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="zai-org/GLM-5.3",
    temperature=0.9
   
)

model = ChatHuggingFace(llm=llm)

response = model.invoke("what is transformers? explain like I am 5 years old kid with real life analogy")

print(response.content)