from fastapi import FastAPI
from graph import app as graph_app
from state import State

app = FastAPI()

@app.post("/healthy")
async def health_check():
    return {"status": "healthy_parallel_graphs"}



@app.post("/PlanTrip")
async def plan_trip(user_prompt: str):
    initial_state: State = {
        "user_prompt": user_prompt
    }
    final_state = graph_app.invoke(initial_state)
    return final_state

