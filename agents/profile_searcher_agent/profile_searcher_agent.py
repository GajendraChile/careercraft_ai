
from strands import Agent
from strands.models.litellm import LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()
MODEL = os.getenv("MODEL_CLAUDE_SONNET")
litellm_model = LiteLLMModel(
    model_id=MODEL,
    params={
        #"max_tokens": 1000,
        "temperature": 0.3,
    }
)

def create_profile_searcher_agent(tools):
    agent = Agent(
        model = litellm_model,
        name="Profile_Searcher",
        description="Searcher profiles according to the job description",
        system_prompt = '''
        You are a profile searcher agent. You will receive a job description.

        Use the hr_system tool to search for the most suitable profiles for the job. 
        
        ** The profiles should strictly match all the following conditions
           - Condition 1: The profiles should strictly match all the primary skills
           - Condition 2: The profiles should strictly match atleast 50 percent of the secondary skills.

        The profiles that are the best match should be categorized as Tier 1
        The profiles that are the nearest match should be categorized as Tier 2
        The average match score for each profile should be strictly above 50 percent
        For each suitable profile, return only the following in JSON format:
        - Name
        - Skills Matching: The skills that match with the JD.
        - Match Score (in percentage).
        - Tier
        - Reason for Suggestion (max 50 characters): A short reason why this profile matches the job.

        ** Do not include any other fields or any other additional details.
        If no suitable profiles are found, return an empty list.
        ''',

        tools=tools)
    print("Agent Initialization complete")
    return agent
