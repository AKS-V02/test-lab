import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrock


# Load environment variables
load_dotenv(find_dotenv())

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

# modelId = "amazon.titan-text-express-v1"
# modelArg = {"maxTokenCount":512,"stopSequences":[],"temperature":0.0,"topP":0.01}

modelId = "meta.llama3-8b-instruct-v1:0"
modelArg = {"max_gen_len":512,"temperature":0.0,"top_p":0.001}

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



#!New Imports
from langchain_aws.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader # pip install pypdf


embed_model_id = "amazon.titan-embed-text-v2:0"

embeddings = BedrockEmbeddings(region_name=os.getenv("AWS_REGION"), model_id=embed_model_id)

# 1. Load a pdf file
loader = PyPDFLoader("./data/react-paper.pdf")
docs = loader.load()

# 2. Split the document into chunks
# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)
splits = text_splitter.split_documents(docs)

# Install faiss vector store...or chroma! pip install chromadb
from langchain_chroma import Chroma
persist_directory = './vector_data/db/chroma/'
# !rm -rf ./data/db/chroma  # remove old database files if any
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings, # becrock embeddings
    persist_directory= persist_directory,
    collection_name="react_paper"
)
# vectorstore.persist() # save this for later usage!

## load the persisted db
vector_store = Chroma(persist_directory=persist_directory,
                      embedding_function=embeddings)


# make a retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
docs = retriever.invoke("Tell me more about ReAct prompting")
# print(retriever.search_type)
print(docs[0].page_content)


# # Make a chain to answer questions
# from langchain.chains import RetrievalQA

# qa_chain = RetrievalQA.from_chain_type(
#     llm=chatLlm,
#     chain_type="stuff",
#     retriever=retriever,
#     verbose=True,
#     return_source_documents=True
    
# )

# ## Cite sources - helper function to prettyfy responses
# def process_llm_response(llm_response):
#     print(llm_response['result'])
#     print('\n\nSources:')
#     for source in llm_response["source_documents"]:
#         print(source.metadata['source'])

# query = "tell me more about ReAct prompting"
# llm_response = qa_chain(query)
# print(process_llm_response(llm_response=llm_response))


from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

# # See full prompt at https://smith.langchain.com/hub/rlm/rag-prompt
# # prompt = hub.pull("rlm/rag-prompt")

prompt = ChatPromptTemplate.from_messages([HumanMessagePromptTemplate.from_template("""
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
""")])

print(prompt)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


qa_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | chatLlm
    | StrOutputParser()
)

query = "tell me more about ReAct prompting"

llm_response = qa_chain.invoke(query)
print("===================================================")
print(llm_response)


# from langchain.chains.retrieval import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# # Load docs
# from langchain_community.document_loaders import WebBaseLoader # pip install beautifulsoup4
# from langchain_community.vectorstores import FAISS # pip install faiss-cpu
# # from langchain_text_splitters import RecursiveCharacterTextSplitter

# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
# data = loader.load()

# # Split
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# all_splits = text_splitter.split_documents(data)

# # Store splits
# FAISSvectorstore = FAISS.from_documents(documents=all_splits, embedding=embeddings)

# # See full prompt at https://smith.langchain.com/hub/langchain-ai/retrieval-qa-chat
# # retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# retrieval_qa_chat_prompt = ChatPromptTemplate.from_messages([
#         SystemMessagePromptTemplate.from_template("""
#         Answer any use questions based solely on the context below:

#         <context>
#         {context}
#         </context>
#         """),
#         MessagesPlaceholder("chat_history", optional=True), 
#         HumanMessagePromptTemplate.from_template("{input}")
# ])

# combine_docs_chain = create_stuff_documents_chain(chatLlm, retrieval_qa_chat_prompt)
# rag_chain = create_retrieval_chain(FAISSvectorstore.as_retriever(), combine_docs_chain)

# query = "What are autonomous agents?"

# llm_response = rag_chain.invoke({"input": query})

# print("===================================================")
# print(llm_response)