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
def create_profile_matcher_agent(tools):
    agent = Agent(
      model = litellm_model,
      name="Profile_Matcher",
      description="Matcher profiles according to profiles",
      system_prompt='''
                  You are a profile matcher agent. You will receive a profiles and job description specification.
                  Utilize the feedback_system tool for getting the past performance for evaluation and rating.
                  ** Donot recommend profiles on your own. Just evaluate the provided profiles.
                  Return name, profile description, experience, technologies, ratings(on a scale of 10) for each in bullet points
                  
                  ** Strictly keep the evaluation response for each profile within 150 characters.

      ''',
      tools=tools)
    print("Agent Initialization complete")
    return agent

 