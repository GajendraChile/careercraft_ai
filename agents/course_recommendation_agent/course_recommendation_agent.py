
from strands import Agent
from strands.models.litellm import LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()
MODEL = os.getenv("MODEL_CLAUDE_SONNET")
litellm_model = LiteLLMModel(
    client_args={
        "api_key" : os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    },
    # **model_config
    model_id=MODEL,
    params={
        #"max_tokens": 1000,
        "temperature": 0.3,
    }
)

def create_course_recommendation_agent(tools):
    agent = Agent(
        model = litellm_model,
        name="Course_Recommender",
        description="Recommends courses for filling skill gaps and upskilling",
        system_prompt = '''
        You are a course recommendation agent. You will receive a job description and profile data.

        Use the lms tool to search for courses that will fill skill gaps. 

        For each suitable profile, return only the following in JSON format:
        - Name
        - Courses: Courses that will help fill skill gaps.
        - Reason for Suggestion (max 50 characters): A short reason why this course helps fill skill gap.

        ** Do not include any other fields or any other additional details.
        If no suitable profiles are found, return an empty list.
        ''',

        tools=tools)
    print("Agent Initialization complete")
    return agent

print("Agent Initialization complete")

  