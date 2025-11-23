from typing import TypedDict

class State(TypedDict):
    user_prompt: str
    outline: str
    blog: str
    score: int
    feedback: str