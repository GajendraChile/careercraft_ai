from fastapi import FastAPI, File, UploadFile, Form
from uuid import uuid4
import os, re, html, json
from cloudpathlib import CloudPath
from dotenv import load_dotenv
from planner_agent import JDAnalyserAgent
from fastapi.middleware.cors import CORSMiddleware
from litellm import completion

load_dotenv()

model = os.getenv("MODEL_CLAUDE_SONNET")
bucket_initials = os.getenv("BUCKET_INITIALS")
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_REGION_NAME"] = os.getenv("AWS_REGION_NAME")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your bucket name here
BUCKET_NAME = os.getenv("BUCKET_NAME")

jd_agent = JDAnalyserAgent()

def get_summary(json_str):
    prompt = f'''
        Generate a short and concise summary of the following Text. 
        Focus on capturing the key information and summary each point consicely.
        The summary should have all the keys mentioned in proper order.
        ** Text: {json_str}
    '''
    response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
    return response.choices[0].message.content


@app.post("/planner_agent/")
def upload_file(user_query: str = Form(...), file: UploadFile = File(...)):
    try:
        #Generate unique file name for the file
        unique_filename = f"{uuid4()}/{file.filename}"
        file_uri = f"{bucket_initials}{BUCKET_NAME}/{unique_filename}"
        cloud_path = CloudPath(file_uri)
        cloud_path.write_bytes(file.file.read())
        print(f"File uploaded to: {file_uri}")
        result = jd_agent.agent(file_uri)
        print(f"result---------------------------------------------: {result}")
        agent_response = result.message["content"][0]["text"]
        print(f"Agent Response in api = {agent_response}")
        try:
            match = re.search(r"```json\n(.*?)```", agent_response, re.DOTALL)
            if not match:
                # Try fallback: extract content between first [ and last ]
                match = re.search(r"(\[.*\])", agent_response, re.DOTALL)
            if match:
                json_str = match.group(1)
                # result = json.loads(json_str)
                result = get_summary(json_str)
                print("---------------------------------------------------")
                print(f"Result Summary :{result}")
                return {"result": result}
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", e)
            return {"Error": e}
    except Exception as e:
        return {"error": str(e)}
    