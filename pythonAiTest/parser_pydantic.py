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
There will be 5 of us on this vacation trip.
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

cities_to_visit: extract the cities they are going to visit. If there are more than 
one, put them in square brackets like '["cityone", "citytwo"].

Format the output as JSON with the following keys:
leave_time
leave_from
cities_to_visit

email: {email}
"""


# Imports
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field, field_validator
from typing import List


# Define desired data structure
class VacationInfo(BaseModel):
    leave_time: str = Field(description="When they are leaving. It's usually")
    leave_from: str = Field(description="Where are they leaving from.\
                                          it's a city, airport or state, or province")
    cities_to_visit: List = Field(description="The cities, towns they will be visiting on \
                                        their trip. This needs to be in a list")
    num_people: int = Field(description="this is an integer for a number of people on this trip")
    
    # you can add custom validation logic...
    @field_validator('num_people')
    def check_num_people(cls, field):
        if field <=0:
            raise ValueError("Badly formatted number")
        return field


    # setup a parser and inect the instructions
pydantic_parser = PydanticOutputParser(pydantic_object=VacationInfo)
format_instructions = pydantic_parser.get_format_instructions()
    
    
# reviewed email template - we updated to add the {format_instructions}
email_template_revised = """
From the following email, extract the following information regarding 
this trip.

email: {email}

{format_instructions}
"""


updated_prompt = ChatPromptTemplate.from_template(template=email_template_revised)
meassages = updated_prompt.format_messages(email=email_response,
                                           format_instructions=format_instructions)

# format_response = chatLlm.invoke(meassages)

# print(format_response.content)
# print("=====================================")

# vacation = pydantic_parser.parse(format_response.content)
# print(type(vacation))
chain = chatLlm | StrOutputParser() | pydantic_parser.parse
vacation = chain.invoke(meassages)
print(vacation)
# print(vacation.cities_to_visit)
for item in vacation.cities_to_visit:
    print(f"Cities: {item}")
    

