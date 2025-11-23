from langgraph.graph import StateGraph, START, END
from state import State
from nodes import final_node, budject_node, itinerary_node, risk_assessment_node




graph = StateGraph(State)


graph.add_node("Budject Node", budject_node)
graph.add_node("Itinerary Node", itinerary_node)
graph.add_node("Risk Assessment Node", risk_assessment_node)
graph.add_node("Final Node", final_node)



graph.add_edge(START, "Budject Node")
graph.add_edge(START, "Itinerary Node")
graph.add_edge(START, "Risk Assessment Node")
graph.add_edge("Budject Node", "Final Node")
graph.add_edge("Itinerary Node", "Final Node")
graph.add_edge("Risk Assessment Node", "Final Node")
graph.add_edge("Final Node", END)

app = graph.compile()

