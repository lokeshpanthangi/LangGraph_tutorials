from fastapi import FastAPI
from graph import app as graph_app
from state import State

app = FastAPI()

@app.post("/healthy")
async def health_check():
    return {"status": "healthy_iterative_graphs"}



@app.post("/GenerateTweet")
async def generate_tweet(user_prompt: str):
    initial_state: State = {
        "user_prompt": user_prompt,
        "iteration": 0,
        "max_iterations": 5
    }
    final_state = graph_app.invoke(initial_state)
    return final_state

