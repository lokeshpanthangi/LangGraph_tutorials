from state import State
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file



model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")



# Define structured output models for each node

class BudjectOutput(BaseModel):
    budject_feedback: str
    budject_split: str
    budject_flags: bool

class ItineraryOutput(BaseModel):
    travel_stay : str
    activites : str
    plans: str

class RiskAssessmentOutput(BaseModel):
    risk_score: int
    risk_feedback: str
    Warnings: str

class FinalOutput(BaseModel):
    final_score: int
    final_feedback: str
    recommendations: str



# Create structured output models for each node

structured_budject_model = model.with_structured_output(BudjectOutput)
structured_itinerary_model = model.with_structured_output(ItineraryOutput)
structured_risk_model = model.with_structured_output(RiskAssessmentOutput)
structured_final_model = model.with_structured_output(FinalOutput)




# Define node functions

def budject_node(state: State) -> State:
    query = state["user_prompt"]

    prompt = f"""Based on the following user prompt, provide budget feedback, a budget split, and flag any potential budget issues if the users plan and Budject and Budject wont cover it.
    This is his Query : {query}"""

    budject_result = structured_budject_model.invoke(prompt)

    state["budject_feedback"] = budject_result.budject_feedback
    state["budject_split"] = budject_result.budject_split
    state["budject_flags"] = budject_result.budject_flags

    return {"budject_feedback": state["budject_feedback"],
            "budject_split": state["budject_split"],
            "budject_flags": state["budject_flags"]}


def itinerary_node(state: State):
    query = state["user_prompt"]

    prompt = f"""Based on the following user prompt, create a travel and stay plan, activities, and overall plans.
    This is his Query : {query}"""

    itinerary_result = structured_itinerary_model.invoke(prompt)

    state["travel_stay"] = itinerary_result.travel_stay
    state["activites"] = itinerary_result.activites
    state["plans"] = itinerary_result.plans

    return {"travel_stay": state["travel_stay"],
            "activites": state["activites"],
            "plans": state["plans"]}


def risk_assessment_node(state: State):
    query = state["user_prompt"]

    prompt = f"""Based on the following user prompt, provide a risk score, risk feedback, and warnings.
    This is his Query : {query}"""

    risk_result = structured_risk_model.invoke(prompt)

    state["risk_score"] = risk_result.risk_score
    state["risk_feedback"] = risk_result.risk_feedback
    state["Warnings"] = risk_result.Warnings

    return {"risk_score": state["risk_score"],
            "risk_feedback": state["risk_feedback"],
            "Warnings": state["Warnings"]}


def final_node(state: State):
    budject_feedback = state["budject_feedback"]
    travel_stay = state["travel_stay"]
    risk_feedback = state["risk_feedback"]

    prompt = f"""Based on the following inputs, provide a final score, final feedback, and recommendations.
    Budject Feedback: {budject_feedback}
    Travel and Stay: {travel_stay}
    Risk Feedback: {risk_feedback}"""

    final_result = structured_final_model.invoke(prompt)

    state["final_score"] = final_result.final_score
    state["final_feedback"] = final_result.final_feedback
    state["recommendations"] = final_result.recommendations

    return {"final_score": state["final_score"],
            "final_feedback": state["final_feedback"],
            "recommendations": state["recommendations"]}