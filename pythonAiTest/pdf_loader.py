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

from langchain_community.document_loaders import PyPDFLoader # pip install pypdf

loader = PyPDFLoader("./data/react-paper.pdf")
pages = loader.load()

# print(len(pages))

page = pages[0]
# print(pages)
print(page.page_content[0:700]) # first 700 characters on the page
print(page.metadata)