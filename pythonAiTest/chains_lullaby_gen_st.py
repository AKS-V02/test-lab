import os
from dotenv import find_dotenv, load_dotenv
import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import streamlit as st 

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




def generate_lullaby(location, name, language):
    
    template = """ 
        As a children's book writer, please come up with a simple and short (90 words)
        lullaby based on the location
        {location}
        and the main character {name}
        
        STORY:
    """

    prompt = PromptTemplate(input_variables=["location", "name"],
                            template=template)

    chain_story = prompt | chatLlm | StrOutputParser()


    # ======= Sequential Chain =====
    # chain to translate the story to Portuguese
    template_update = """
    Translate the {story} into {language}.  Make sure 
    the language is simple and fun.

    TRANSLATION:
    """

    prompt_translate = PromptTemplate(input_variables=["story", "language"],
                                    template=template_update)

    chain_translate = prompt_translate | chatLlm | StrOutputParser()


    # ==== Create the Sequential Chain ===
    overall_chain = (RunnablePassthrough().assign(story=chain_story) | RunnablePassthrough().assign(translated=chain_translate))

    response = overall_chain.invoke({"location": location, 
                            "name": name,
                            "language": language
                            })
    
    
    
    return response


def main():
    st.set_page_config(page_title="Generate Children's Lullaby",
                       layout="centered")
    st.title("Let AI Write and Translate a Lullaby for You 📖")
    st.header("Get Started...")
    
    location_input = st.text_input(label="Where is the story set?")
    main_character_input = st.text_input(label="What's the main charater's name")
    language_input = st.text_input(label="Translate the story into...")
    
    submit_button = st.button("Submit")
    if location_input and main_character_input and language_input:
        if submit_button:
            with st.spinner("Generating lullaby..."):
                response = generate_lullaby(location=location_input,
                                            name= main_character_input,
                                            language=language_input)
                
                with st.expander("English Version"):
                    st.write(response['story'])
                with st.expander(f"{language_input} Version"):
                    st.write(response['translated'])
                
            st.success("Lullaby Successfully Generated!")
    
    
    
    
    
    
    
    















 #Invoking main function
if __name__ == '__main__':
    main()  