import os
from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate


# Load environment variables
load_dotenv(find_dotenv())

# client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

modelId = "amazon.titan-text-express-v1"
modelArg = {"maxTokenCount":512,"stopSequences":[],"temperature":0,"topP":0.01}

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

email_response = """
Here's our itinerary for our upcoming trip to Europe.
We leave from Denver, Colorado airport at 8:45 pm, and arrive in Amsterdam 10 hours later
at Schipol Airport.
We'll grab a ride to our airbnb and maybe stop somewhere for breakfast before 
taking a nap.

Some sightseeing will follow for a couple of hours. 
We will then go shop for gifts 
to bring back to our children and friends.  

The next morning, at 7:45am we'll drive to to Belgium, Brussels - it should only take aroud 3 hours.
While in Brussels we want to explore the city to its fullest - no rock left unturned!

"""

email_template = """
From the following email, extract the following information:

leave_time: when are they leaving for vacation to Europe. If there's an actual
time written, use it, if not write unknown.

leave_from: where are they leaving from, the airport or city name and state if
available.

cities_to_visit: extract the cities they are going to visit. 
If there are more than one, put them in square brackets like '["cityone", "citytwo"].

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
"""



# desired_format = {
#     "leave_time": "8:45 pm",
#     "leave_from": "Denver, Colorado",
#     "cities_to_visit": ["Amsterdam", "Brussels"]
# }

prompt_template = ChatPromptTemplate.from_template(email_template)
#print(prompt_template)

messages = prompt_template.format_messages(email=email_response)
# response = chatLlm.invoke(messages)

# print(response.content)

# ==== Langchain Parsers ====
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser, OutputFixingParser

leave_time_schema = ResponseSchema(name="leave_time",
                                   description="When they are leaving. \
                                       It's usually a numberical time of the day. \
                                           If not available wirte n/a")
leave_from_schema = ResponseSchema(name="leave_from",
                                      description="Where are they leaving from.\
                                          it's a city, airport or state, or province")
cities_to_visit_schema = ResponseSchema(name="cities_to_visit",
                                    description="The cities, towns they will be visiting on \
                                        their trip. This needs to be in a list")

response_schema = [
    leave_time_schema,
    leave_from_schema,
    cities_to_visit_schema
]

# setup the output parser
output_parser = StructuredOutputParser.from_response_schemas(response_schema)

format_instructions = output_parser.get_format_instructions()
# print(format_instructions)

# reviewed email template - we updated to add the {format_instructions}
email_template_revised = """
From the following email, extract the following information:

leave_time: when are they leaving for vacation to Europe. If there's an actual
time written, use it, if not write unknown.

leave_from: where are they leaving from, the airport or city name and state if
available.

cities_to_visit: extract the cities they are going to visit. If there are more than 
one, put them in square brackets like '["cityone", "citytwo"].

Format the output as a JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
{format_instructions}
"""

updated_prompt = ChatPromptTemplate.from_template(template=email_template_revised)
messages = prompt_template.format_messages(email=email_response,
                                           format_instructions=format_instructions)

response = chatLlm.invoke(messages)

print(response.content)
print("=====================================")
print(type(response.content))

from langchain_core.exceptions import OutputParserException

output_dict = {}

try:
    output_dict = output_parser.parse(response.content) # parse into dict does not work with aws titen text express 
except OutputParserException as e:
    print(e)
    fix_parser = OutputFixingParser.from_llm(parser=output_parser, llm=chatLlm)
    output_dict = fix_parser.parse(response.content)

print(type(output_dict))
print(f"Cities:::: {output_dict['cities_to_visit'][0]}")

