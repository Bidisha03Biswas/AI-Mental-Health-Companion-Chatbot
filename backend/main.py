#Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from backend.ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    try:
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)

        # Fallbacks for empty responses
        if not final_response:
            final_response = "I'm here with you. Can you tell me a little about how you're feeling right now?"
        if not tool_called_name:
            tool_called_name = "None"

        return {"response": final_response, "tool_called": tool_called_name}

    except Exception as e:
        # Always return JSON even on exceptions
        return {"response": f"Error: {str(e)}", "tool_called": "None"}


#Step3: Sent response to the frontend
    return {"response": final_response,
            "tool_called": tool_called_name}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

