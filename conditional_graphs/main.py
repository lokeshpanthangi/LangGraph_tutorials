from fastapi import FastAPI
from graph import app as graph_app
from state import State

app = FastAPI()

@app.post("/healthy")
async def health_check():
    return {"status": "healthy_conditional_graphs"}



@app.post("/supportRequest")
async def support_request(user_prompt: str):
    initial_state: State = {
        "user_prompt": user_prompt
    }
    final_state = graph_app.invoke(initial_state)
    return final_state

