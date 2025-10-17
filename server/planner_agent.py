from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools.a2a_client import A2AClientToolProvider
import os
from strands import tool
from dotenv import load_dotenv
import logging
import io
from pypdf import PdfReader
from litellm import completion
from cloudpathlib import CloudPath

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_REGION_NAME"] = os.getenv("AWS_REGION_NAME")

profile_search_agent_url = os.getenv("PROFILE_SEARCH_AGENT_URL")
profile_matcher_agent_url = os.getenv("PROFILE_MATCHER_AGENT_URL")
course_recommender_agent_url = os.getenv("COURSE_RECOMMENDER_AGENT_URL")
class JDAnalyserAgent:
    def __init__(self):
        self.model_id = os.getenv("MODEL_CLAUDE_SONNET")
        self.provider = A2AClientToolProvider(known_agent_urls=[profile_search_agent_url, profile_matcher_agent_url,course_recommender_agent_url])
        self.litellm_model = LiteLLMModel(
            client_args={
                "aws_access_key_id" : os.getenv("AWS_ACCESS_KEY_ID"),
                "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "aws_region_name" : os.getenv("AWS_REGION_NAME")
            },
            model_id=self.model_id,
            params={
                "temperature": 0.3,
            }
        )
        # self.bucket_name = "aws_hackathon_file_store"
        self.agent = Agent(
            model=self.litellm_model,
            system_prompt="""You are an agent that analyses Job descriptions and extracts key details from it.
            You receive a file_uri from the user. Strictly invoke the tool 'analyse_jd' with the file_uri.
            After receiving the JD specification from the tool perform the following steps:

            ## Step 1: Search profiles that match the job description provided by user using profile_searcher agent. 
            ## Step 2: Evaluate the profiles using profile_matcher agent.
            ## Step 2: Recommend relevant courses to fill skill gaps using course_recommender agent.

            ** Donot extract data on your own. Always use the tool to extract the details.
            **Donot make any changes to the response received from the tool.

            Return the data to the user in JSON format with the following keys:
            - Name
            - Performance Rating
            - Outcome (Recommended/Not Recommended)
            - Evaluation Comments
            - Recommended Courses
            """,
            tools=[self.analyse_jd, self.provider.tools]
        )
    @tool
    def analyse_jd(self, file_uri: str) -> str:
        """
        Tool to analyse JD and extract key details
        """
        print("Inside Tool")
        try:
            cloud_path = CloudPath(file_uri)
            # Download the PDF file into memory
            pdf_bytes = io.BytesIO(cloud_path.read_bytes())
            print(f"Downloaded '{file_uri}' into memory.")
        
            # Use pypdf to read the PDF directly from the BytesIO object
            reader = PdfReader(pdf_bytes)
        
            # Extract and print text from pages
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            print("--- Extracted Text ---")
            print(text)
            print("--------------------------------------------------")
            prompt = f'''
            ```Text : {text} ```

            Extract and **summarize concisely** the following key specifications from the provided text. Use your own words to paraphrase where appropriate, but do not invent or infer information that is not present in the text.

            Required fields:
            - Job Title
            - Responsibilities
            - Primary Skills (These are the skills that match exactly to the job title and description)
            - Secondary Skills (These are skills other than the primary skills)
            - Preferred Qualifications
            - Experience Level
            - Location
            - Employment Type
            - Certifications or Tools Mentioned

            **Instructions:**
            - Only include the fields listed above.
            - If a field is not mentioned in the text, return "NONE" for that field.
            - Keep responses brief and paraphrased — avoid copying full sentences unless necessary.
            - Format the output strictly in JSON.

            '''

            response = completion(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            print(f"Response inside tool = {response}")
            return response
        except Exception as e:
            print(f"An error occurred: {e}")

    


