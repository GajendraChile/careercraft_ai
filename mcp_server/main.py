from services.LMS.lms import LMS
from services.HR_System.hrsystem import HRSystem
from services.Feedback_System.feedbacksystem import FeedbackSystem
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp_server")

lms = LMS()
hr_system = HRSystem()
feedback_system = FeedbackSystem()

@mcp.tool()
def lms_tool(query : str) -> dict:
    response = " No response found"
    try:
        response = lms.search(query)
    except Exception as e:
        response = str(e)
    return {"Response" : response}

@mcp.tool()
def hr_system_tool(query : str) -> dict:
    response = " No response found"
    try:
        response = hr_system.search(query)
    except Exception as e:
        response = str(e)
    return {"Response" : response}

@mcp.tool()
def feedback_system_tool(query : str) -> dict:
    response = " No response found"
    try:
        response = feedback_system.search(query)
    except Exception as e:
        response = str(e)
    return {"Response" : response}

app = mcp.streamable_http_app()