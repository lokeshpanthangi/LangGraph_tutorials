from state import State
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")



def outline_gen(state: State) -> State:
    query = state["user_prompt"]

    prompt = f"""Create a detailed outline for a blog post based on the following user prompt:
    {query}"""

    outline = model.invoke(prompt)

    state["outline"] = outline.content

    return state


def blog_gen(state: State) -> State:
    outline = state["outline"]

    prompt = f"""Write a comprehensive blog post based on the following outline:
    {outline}"""

    blog = model.invoke(prompt)

    state["blog"] = blog.content

    return state


def blog_evaluator(state: State) -> State:
    blog = state["blog"]

    outline = state["outline"]

    prompt = f"""Evaluate the following blog post based on how well it adheres to the provided outline.
    Outline:
    {outline}

    Blog Post:
    {blog}

    Provide a score from 1 to 10 and constructive feedback.
    
    reply strictly in the JSON format:
    {{
        "score": <score>,
        "feedback": "<feedback>"
    }}"""

    evaluation_str = model.invoke(prompt).content

    state["score"] = json.loads(evaluation_str)["score"]
    state["feedback"] = json.loads(evaluation_str)["feedback"]

    return state