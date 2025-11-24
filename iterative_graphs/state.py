from typing import TypedDict

class State(TypedDict):
    user_prompt : str
    tweet : str
    status : str
    feedback : str
    iteration : int
    max_iterations : int