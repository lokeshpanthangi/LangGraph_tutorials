from state import State
from typing import Literal
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel


class RoutingOutput(BaseModel):
    user_issue: str
    route_to: Literal["Technical Support", "Billing", "General Inquiry"]



load_dotenv()  # Load environment variables from .env file
model = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
structured_routing_model = model.with_structured_output(RoutingOutput)







def route_issue(state: State) -> State:
    user_prompt = state["user_prompt"]

    prompt = f"""Based on the following user prompt,find out exactly whats the users issue is and  determine the appropriate department to route the issue to: Technical Support, Billing, or General Inquiry.
    User Issue:
    {user_prompt}
    Reply strictly in the JSON format:
    {{
        "user_issue": "<issue_description>",
        "route_to": "<department>"
    }}"""

    routing_result = structured_routing_model.invoke(prompt)

    state["route_to"] = routing_result.route_to
    state["user_issue"] = routing_result.user_issue

    return state


def technical_support_node(state: State) -> State:
    issue = state["user_issue"]

    prompt = f"""Provide a detailed response to the following technical support issue:
    {issue}"""

    response = model.invoke(prompt)

    state["support_response"] = response.content

    return state


def billing_node(state: State) -> State:
    issue = state["user_issue"]

    prompt = f"""Provide a detailed response to the following billing issue:
    {issue}"""

    response = model.invoke(prompt)

    state["support_response"] = response.content

    return state


def general_inquiry_node(state: State) -> State:
    issue = state["user_issue"]

    prompt = f"""Provide a detailed response to the following general inquiry:
    {issue}"""

    response = model.invoke(prompt)

    state["support_response"] = response.content

    return state
