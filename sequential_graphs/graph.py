from langgraph.graph import StateGraph, START, END
from state import State
from nodes import outline_gen, blog_gen, blog_evaluator



graph = StateGraph(State)

graph.add_node("Outline Generation", outline_gen)
graph.add_node("Blog Generation", blog_gen)
graph.add_node("Blog Evaluation", blog_evaluator)

graph.add_edge(START, "Outline Generation")
graph.add_edge("Outline Generation", "Blog Generation")
graph.add_edge("Blog Generation", "Blog Evaluation")
graph.add_edge("Blog Evaluation", END)

app = graph.compile()

