#from langchain.agents import tool
from langchain_core.tools import tool
from backend.tools import query_medgemma, call_emergency
@tool                          #it is a decorator that converts any function into a LangChain tool.
def ask_mental_health_specialist(query: str) -> str:
     """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
     return query_medgemma(query)

@tool
def emergency_call_tool(phone: str) -> str:
    """
    Use ONLY if user expresses suicidal thoughts, self-harm intent, or immediate danger.
    """
    return call_emergency(phone)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (                #just returning a dummy response.
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


#Step1: Create an AI agent and link to backend 
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from groq import Groq
from backend.config import GROQ_API_KEY
from langchain_groq import ChatGroq
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langgraph.prebuilt import create_react_agent
llm = ChatGroq(
    model="gpt-oss-120b",
    temperature=0.2,
    api_key=GROQ_API_KEY
)


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.2, api_key=GROQ_API_KEY)  #Using Groq API key for GPT-OSS-120B model
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
Do NOT introduce yourself or state a name unless the user explicitly asks.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `locate_therapist_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: Use this immediately if the user expresses suicidal thoughts, self-harm intentions, or is in crisis.

Always take necessary action. Respond kindly, clearly, and supportively.
"""
def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        #Check if a tool is called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        #Check if  agent returned a final response
        agent_date = s.get('agent')
        if agent_date:
            messages = agent_date.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response

"""
if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print(f"Received user input: {user_input[:200]}...") # Log first 200 characters of input
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        stream = graph.stream(inputs, stream_mode="updates")
        #for s in stream:
            #print(s)
        tool_called_name, final_response= parse_response(stream)
        print("TOOL CALLED:", tool_called_name)
        print("ANSWER: ", final_response)

"""