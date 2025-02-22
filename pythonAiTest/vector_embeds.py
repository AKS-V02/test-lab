import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrock


# Load environment variables
load_dotenv(find_dotenv())

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

modelId = "amazon.titan-text-express-v1"
modelArg = {"maxTokenCount":512,"stopSequences":[],"temperature":0.0,"topP":0.01}

# modelId = "meta.llama3-8b-instruct-v1:0"
# modelArg = {"max_gen_len":512,"temperature":0.0,"top_p":0.001}

# llm = BedrockLLM(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#                 aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#                 region=os.getenv("AWS_REGION"),
#                 model_id=modelId,
#                 model_kwargs=modelArg)

chatLlm = ChatBedrock(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region=os.getenv("AWS_REGION"),
                    model_id=modelId,
                    model_kwargs=modelArg)

from langchain_aws.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader # pip install pypdf
# import boto3

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

embed_model_id = "amazon.titan-embed-text-v2:0"

embeddings = BedrockEmbeddings(region_name=os.getenv("AWS_REGION"), model_id=embed_model_id)

# 1. Load a pdf file
loader = PyPDFLoader("./data/react-paper.pdf")
docs = loader.load()

# 2. Split the document into chunks
# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)
splits = text_splitter.split_documents(docs)
print(len(splits))
# =============== ==================== # 


# Real-world exampl with embeddings!
# Chroma db = #pip install langchain_chroma
from langchain_chroma import Chroma
persist_directory = "./vector_data/db/chroma"

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings, # bedrock embeddings
    persist_directory=persist_directory
    )
# print(vectorstore._collection.count())

query = "what do they say about ReAct prompting method?"

docs_resp = vectorstore.similarity_search(query=query, k=3)

print(len(docs_resp))
print(docs_resp[0].page_content)

# vectorstore.persist() # save this for later usage!


















# Embeddings - simpler example - compare similarity etc.
# text1 = "Kitty"
# text2 = "Rock"
# text3 = "Cat"

# embed1 = embeddings.embed_query(text1)
# embed2 = embeddings.embed_query(text2)
# embed3 = embeddings.embed_query(text3)
# # print(f"Embed! == {embed1}")
# # print(f"Embed! == {embed2}")
# # print(f"Embed! == {embed3}")
# import numpy as np
# similarity = np.dot(embed1, embed3)
# print(f"Similary %: {similarity*100}")

