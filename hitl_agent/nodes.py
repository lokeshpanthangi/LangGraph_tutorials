from typing import TypedDict, Annotated
from tools import ALL_TOOLS
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[str], add_messages]
    user_prompt: str
    tool_selected: str
    tool_response: str
    next_node: str
    final_response: str



model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)


tools = ALL_TOOLS

input_model = model.bind_tools(tools)

def input_node(state: State):
    return input_model(
        messages=state["messages"],
        user_prompt=state["user_prompt"],
    )