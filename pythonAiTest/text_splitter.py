from langchain.text_splitter import CharacterTextSplitter

# 1. CharacterTextSplitter
with open("./data/i-have-a-dream.txt") as paper:
    speech = paper.read()
    
text_splitter = CharacterTextSplitter(
    
    chunk_size = 100,
    chunk_overlap = 20,
    length_function = len
)

texts = text_splitter.create_documents([speech])
print(texts[0])



