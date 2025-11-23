from fastapi import FastAPI
from graph import app as graph_app

app = FastAPI()

@app.post("/healthy")
async def health_check():
    return {"status": "healthy_sequential_graphs"}


@app.post("/GenerateBlogPost")
async def generate_blog_post(user_prompt: str):
    initial_state = {
        "user_prompt": user_prompt,
        "outline": "",
        "blog": "",
        "score": 0,
        "feedback": ""
    }
    final_state = graph_app.invoke(initial_state)
    return final_state

