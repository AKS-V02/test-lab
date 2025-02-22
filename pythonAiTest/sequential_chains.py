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


from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

template = """ 
 As a children's book writer, please come up with a simple and short (90 words)
 lullaby based on the location
 {location}
 and the main character {name}
 
 STORY:
"""

prompt = PromptTemplate(input_variables=["location", "name"],
                        template=template)

# chain_story = LLMChain(llm=open_ai, prompt=prompt, 
#                        output_key="story",
#                        verbose=True)

chain_story = prompt | chatLlm | StrOutputParser()

# story = chain_story({"location": "Zanzibar", "name": "Maya"})
# print(story['text'])

# ======= Sequential Chain =====
# chain to translate the story to Portuguese
template_update = """
Translate the {story} into {language}.  Make sure 
the language is simple and fun.

TRANSLATION:
"""

prompt_translate = PromptTemplate(input_variables=["story", "language"],
                                  template=template_update)

# chain_translate = LLMChain(
#     llm=open_ai,
#     prompt=prompt_translate,
#     output_key="translated"
# )
chain_translate = prompt_translate | chatLlm | StrOutputParser()

# overall_chain = SequentialChain(
#     chains=[chain_story, chain_translate],
#     input_variables=["location", "name", "language"],
#     output_variables=["story", "translated"], # return story and the translated variables!
#     verbose=True
# )

overall_chain = (RunnablePassthrough().assign(story=chain_story) | RunnablePassthrough().assign(translated=chain_translate))

response = overall_chain.invoke({"location": "Magical", 
                          "name": "Karyna",
                          "language": "Russian"
                          })
print(f"English Version ====> { response['story']} \n \n")
print(f"Translated Version ====> { response['translated']}")


