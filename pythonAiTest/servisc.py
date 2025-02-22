import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import BedrockLLM, ChatBedrock
from langchain_aws.chat_models import bedrock
from langchain_core import document_loaders
import langchain_text_splitters as CharacterTextSplitter 
from langchain_aws.vectorstores import inmemorydb
from langchain_aws.embeddings import bedrock
from langchain.prompts import PromptTemplate, ChatPromptTemplate

# import boto3

# Load environment variables
load_dotenv(find_dotenv())

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

modelId = "amazon.titan-text-express-v1"
modelArg = {"maxTokenCount":512,"stopSequences":[],"temperature":0,"topP":0.01}

# modelId = "meta.llama3-8b-instruct-v1:0"
# modelArg = {"max_gen_len":512,"temperature":0,"top_p":0.01}

llm = BedrockLLM(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region=os.getenv("AWS_REGION"),
                model_id=modelId,
                model_kwargs=modelArg)

chatLlm = ChatBedrock(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region=os.getenv("AWS_REGION"),
                    model_id=modelId,
                    model_kwargs=modelArg)


# prompt = "who are you?"

# print(llm.invoke(prompt))
# print("=====================================")
# print(chatLlm.invoke([prompt]).content)


multi_var_prompt = PromptTemplate(
    input_variables=["customerServiceManager", "customerName", "feedbackFromCustomer"], 
    template="""

Human: Create an apology email from the Service Manager {customerServiceManager} to {customerName} in response to the following feedback that was received from the customer: 
<customer_feedback>
{feedbackFromCustomer}
</customer_feedback>

Assistant:"""
)

# Pass in values to the input variables
prompt = multi_var_prompt.format(customerServiceManager="Bob", 
                                 customerName="John Doe", 
                                 feedbackFromCustomer="""Hello Bob,
     I am very disappointed with the recent experience I had when I called your customer support.
     I was expecting an immediate call back but it took three days for us to get a call back.
     The first suggestion to fix the problem was incorrect. Ultimately the problem was fixed after three days.
     We are very unhappy with the response provided and may consider taking our business elsewhere.
     """
     )


# print(llm.invoke(prompt))
print("=====================================")
from langchain_core.messages import HumanMessage


chatTemplate = ChatPromptTemplate.from_template(
"""
translate the following text to French and then translate it to English with tone {tone} : {coustomer_review} 
"""
)



prompt = chatTemplate.format_messages(
    coustomer_review=
    """
    i did not like the room servisces at all. the food was cold and the room was not clean.
    """,
    tone="anger"
)

print(chatLlm.invoke(prompt).content)