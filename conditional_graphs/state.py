from typing import TypedDict

class State(TypedDict):
    user_prompt: str
    
    user_issue: str
    route_to: str

    support_response: str