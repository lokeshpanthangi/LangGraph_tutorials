from typing import TypedDict

class State(TypedDict):
    user_prompt: str
    
    # Budject node result 
    budject_feedback: str
    budject_split: str
    budject_flags: bool

    #iternary node result
    travel_stay : str
    activites : str
    plans: str

    #risk assessment node result
    risk_score: int
    risk_feedback: str
    Warnings: str

    #final node result

    final_score: int
    final_feedback: str
    recommendations: str
