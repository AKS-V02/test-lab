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

from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser


biology_template = """You are a very smart biology professor. 
You are great at answering questions about biology in a concise and easy to understand manner. 
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{input}"""

biology_prompt = ChatPromptTemplate.from_template(template=biology_template)
biology_chain = biology_prompt | chatLlm | StrOutputParser()

math_template = """You are a very good mathematician. You are great at answering math questions. 
You are so good because you are able to break down hard problems into their component parts, 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}"""

math_prompt = ChatPromptTemplate.from_template(template=math_template)
math_chain = math_prompt | chatLlm | StrOutputParser()

astronomy_template = """You are a very good astronomer. You are great at answering astronomy questions. 
You are so good because you are able to break down hard problems into their component parts, 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}"""

astronomy_prompt = ChatPromptTemplate.from_template(template=astronomy_template)
astronomy_chain = astronomy_prompt | chatLlm | StrOutputParser()

travel_agent_template = """You are a very good travel agent with a large amount
of knowledge when it comes to getting people the best deals and recommendations
for travel, vacations, flights and world's best destinations for vacation. 
You are great at answering travel, vacation, flights, transportation, tourist guides questions. 
You are so good because you are able to break down hard problems into their component parts, 
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{input}"""

travel_agent_prompt = ChatPromptTemplate.from_template(template=travel_agent_template)
travel_agent_chain = travel_agent_prompt | chatLlm | StrOutputParser()


# prompt_infos = [
#     {
#         "name": "Biology",
#         "description": "Good for answering Biology related questions"
#     },
#     {
#         "name": "math",
#         "description": "Good for answering math questions"
#     },
#     {
#         "name": "astronomy",
#         "description": "Good for answering astronomy questions"
#     },
#     {
#         "name": "travel_agent",
#         "description": "Good for answering travel, tourism and vacation questions"
#     },
# ]

# destination_chains = {}
# for info in prompt_infos:
#     name = info["name"]
#     prompt_template = info["prompt_template"]
#     prompt = ChatPromptTemplate.from_template(template=prompt_template)
#     chain = prompt | chatLlm | StrOutputParser()
#     destination_chains[name] = chain
  
# Setup the default chain  
default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = default_prompt | chatLlm | StrOutputParser()

# from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
# from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
# from langchain.chains.router import MultiPromptChain

from operator import itemgetter
from typing import Literal

from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict
from langchain_core.runnables import RunnableConfig


# destinations_details = [f"{p['name']}: {p['description']}" for p in prompt_infos]
# destinations_str = "\n".join(destinations_details)

destinations = Literal["biology", "math", "astronomy", "travel_agent"]

# destinations_names = [p["name"] for p in prompt_infos]

# router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)

# router_prompt = PromptTemplate(
#     template=router_template,
#     input_variables=["input"],
#     output_parser=RouterOutputParser()
# )

from langchain.output_parsers import StructuredOutputParser, ResponseSchema, OutputFixingParser
from langchain_core.exceptions import OutputParserException

destination_schema = ResponseSchema(name="destination",
                                    description="The best expert for the query ")

response_schema = [
    destination_schema
]

# setup the output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schema)

format_instructions = output_parser.get_format_instructions()

router_template = """
Answer this question in below provided Single JSON Object format: Who is the best expert from the below list for the query?

experts:

"Biology": "Good for answering Biology related questions"

"math": "Good for answering math questions"

"astronomy": "Good for answering astronomy questions"

"travel_agent": "Good for answering travel, tourism and vacation questions"

Query:

{input}

format_instructions:

{format_instructions}

"""

router_prompt = ChatPromptTemplate.from_template(
    template=router_template
)

print(router_prompt)
 
# router_chain = LLMRouterChain.from_llm(
#     llm=chatLlm,
#     prompt=router_prompt,
    
# ) 

# Define schema for output:
# class RouteQuery(TypedDict):
#     """Route query to destination expert."""

#     destination: destinations


# route_chain = router_prompt | chatLlm.with_structured_output(RouteQuery)
def parse_route_output(output):
    try:
        output_dict = output_parser.parse(output) # parse into dict does not work with aws titen text express 
    except OutputParserException as e:
        print(e)
        fix_parser = OutputFixingParser.from_llm(parser=output_parser, llm=chatLlm)
        output_dict = fix_parser.parse(output)
    return output_dict


route_chain = router_prompt | chatLlm | StrOutputParser() | parse_route_output
# chain = MultiPromptChain(
#     router_chain=router_chain,
#     destination_chains=destination_chains,
#     default_chain=default_chain,
#     verbose=True
# )

# For LangGraph, we will define the state of the graph to hold the query,
# destination, and final answer.
class State(TypedDict):
    query: str
    destination: dict
    route_formate: str
    answer: str


# We define functions for each node, including routing the query:
def route_query(state: State, config: RunnableConfig):
    destination = route_chain.invoke({"input": state["query"], "format_instructions": state["route_formate"]}, config=config)
    return {"destination": destination["destination"]}


# And one node for each prompt
def biology(state: State, config: RunnableConfig):
    return {"answer": biology_chain.invoke({"input": state["query"]}, config=config)}


def astronomy(state: State, config: RunnableConfig):
    return {"answer": astronomy_chain.invoke({"input": state["query"]}, config=config)}


def travel_agent(state: State, config: RunnableConfig):
    return {"answer": travel_agent_chain.invoke({"input": state["query"]}, config=config)}


def math(state: State, config: RunnableConfig):
    return {"answer": math_chain.invoke({"input": state["query"]}, config=config)}

def default(state: State, config: RunnableConfig):
    return {"answer": default_chain.invoke({"input": state["query"]}, config=config)}


# We then define logic that selects the prompt based on the classification
def select_node(state: State) -> Literal[destinations, "default"]:
    if state["destination"] in destinations:
        return state["destination"]
    else:
        return "default"


# Finally, assemble the multi-prompt chain. This is a sequence of two steps:
# 1) Select "animal" or "vegetable" via the route_chain, and collect the answer
# alongside the input query.
# 2) Route the input query to chain_1 or chain_2, based on the
# selection.
graph = StateGraph(State)
graph.add_node("route_query", route_query)
graph.add_node("biology", biology)
graph.add_node("math", math)
graph.add_node("travel_agent", travel_agent)
graph.add_node("astronomy", astronomy)
graph.add_node("default", default)

graph.add_edge(START, "route_query")
graph.add_conditional_edges("route_query", select_node)
graph.add_edge("biology", END)
graph.add_edge("math", END)
graph.add_edge("travel_agent", END)
graph.add_edge("astronomy", END)
graph.add_edge("default", END)

app = graph.compile()

# from IPython.display import Image

# Image(app.get_graph().draw_mermaid_png())

state = app.invoke({"query": "I need to go to Kenya for vacation, a family of four. Can you help me plan this trip?", "route_formate": format_instructions})
# state = app.invoke({"query": "How old as the stars?", "route_formate": format_instructions})
print(state["destination"])
print(state["answer"])

# Test
#response = chain.run("I need to go to Kenya for vacation, a family of four. Can you help me plan this trip?")
# response = chain.run("How old as the stars?")
# print(response)