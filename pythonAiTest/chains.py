import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrock


# Load environment variables
load_dotenv(find_dotenv())

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

modelId = "amazon.titan-text-express-v1"
modelArg = {"maxTokenCount":512,"stopSequences":[],"temperature":0.5,"topP":0.5}

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


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# LLMChain
prompt = ChatPromptTemplate.from_messages([("user", "How do you say good morning in {language}")])
    

chain = prompt | chatLlm | StrOutputParser()

out_put = chain.invoke({"language": "German"})

print(out_put) # Guten Morgen!
# chain = LLMChain(llm=open_ai, prompt=prompt)
# print(chain.run(language="German"))

from langchain_core.runnables import RunnablePassthrough

outer_chain = RunnablePassthrough().assign(text=chain)

out_put = outer_chain.invoke({"language": "German"})

print(out_put)# {'language': 'German', 'text': ' "Guten Morgen" is the German equivalent of "Good Morning".'}