# Parallel Graphs - Travel Planning System

## Overview

This project demonstrates a **parallel execution pattern** using LangGraph to build an intelligent travel planning system. Unlike sequential processing, this implementation runs multiple analysis nodes **simultaneously** to gather comprehensive travel insights, then aggregates the results in a final synthesis node.

The system takes a user's travel query and processes it through three parallel pathways:
- **Budget Analysis** - Financial planning and cost breakdown
- **Itinerary Planning** - Travel logistics and activity scheduling  
- **Risk Assessment** - Safety evaluation and warnings

All parallel results converge at a **Final Node** that synthesizes recommendations.

---

## Architecture Diagram

```
                              START
                                |
                    +-----------+-----------+
                    |           |           |
                    v           v           v
            +---------------+   +---------------+   +-------------------+
            | Budget Node   |   | Itinerary     |   | Risk Assessment   |
            |               |   | Node          |   | Node              |
            +-------+-------+   +-------+-------+   +---------+---------+
                    |                   |                     |
                    |                   |                     |
                    +-------------------+---------------------+
                                        |
                                        v
                                +---------------+
                                | Final Node    |
                                | (Synthesis)   |
                                +-------+-------+
                                        |
                                        v
                                       END
```

**Key Feature:** The three analysis nodes execute **in parallel** (simultaneously), not sequentially. This significantly reduces total processing time.

---

## Files

### `state.py`
Defines the `State` TypedDict that holds all data flowing through the graph:
- **Input:** `user_prompt` (user's travel query)
- **Budget Node Output:** `budject_feedback`, `budject_split`, `budject_flags`
- **Itinerary Node Output:** `travel_stay`, `activites`, `plans`
- **Risk Assessment Output:** `risk_score`, `risk_feedback`, `Warnings`
- **Final Node Output:** `final_score`, `final_feedback`, `recommendations`

### `nodes.py`
Implements four node functions with **structured output** using Pydantic models:

1. **`budject_node(state)`** - Analyzes budget requirements
   - Returns: budget feedback, cost breakdown, and flags for potential issues
   - Uses `BudjectOutput` Pydantic model for structured responses

2. **`itinerary_node(state)`** - Plans travel logistics
   - Returns: accommodation plans, activities, and detailed itinerary
   - Uses `ItineraryOutput` Pydantic model

3. **`risk_assessment_node(state)`** - Evaluates travel risks
   - Returns: risk score (numeric), safety feedback, and warnings
   - Uses `RiskAssessmentOutput` Pydantic model

4. **`final_node(state)`** - Synthesizes all parallel outputs
   - Combines budget, itinerary, and risk data
   - Returns: final score, consolidated feedback, and recommendations
   - Uses `FinalOutput` Pydantic model

**Technology:** All nodes use `langchain_openai.ChatOpenAI` with `gpt-4o-mini` model and `.with_structured_output()` for guaranteed JSON schema compliance.

### `graph.py`
Constructs the parallel StateGraph:
```python
# Three nodes fan out from START (parallel execution)
graph.add_edge(START, "Budject Node")
graph.add_edge(START, "Itinerary Node")
graph.add_edge(START, "Risk Assessment Node")

# All converge to Final Node
graph.add_edge("Budject Node", "Final Node")
graph.add_edge("Itinerary Node", "Final Node")
graph.add_edge("Risk Assessment Node", "Final Node")

# Final Node connects to END
graph.add_edge("Final Node", END)
```

### `main.py`
FastAPI application exposing two endpoints:
- **`POST /healthy`** - Health check endpoint
- **`POST /PlanTrip`** - Main endpoint that accepts `user_prompt` parameter and invokes the graph

---

## Requirements

- Python 3.9+
- Dependencies:
  ```
  fastapi
  uvicorn
  python-dotenv
  langchain-openai
  pydantic
  langgraph
  ```

Install command:
```powershell
pip install fastapi uvicorn python-dotenv langchain-openai pydantic langgraph
```

**Environment Setup:**
- Create a `.env` file in the project root with your OpenAI API key:
  ```
  OPENAI_API_KEY=your_key_here
  ```

---

## Running the Service

Start the FastAPI server from the `parallel_graphs` directory:

```powershell
cd parallel_graphs
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

---

## API Usage

### Health Check
```bash
curl -X POST "http://127.0.0.1:8000/healthy"
```
**Response:**
```json
{"status": "healthy_parallel_graphs"}
```

### Plan Trip
```bash
curl -X POST "http://127.0.0.1:8000/PlanTrip?user_prompt=Plan%20a%205-day%20trip%20to%20Tokyo%20with%20$3000%20budget"
```

**Response Structure:**
```json
{
  "user_prompt": "Plan a 5-day trip to Tokyo with $3000 budget",
  "budject_feedback": "...",
  "budject_split": "...",
  "budject_flags": false,
  "travel_stay": "...",
  "activites": "...",
  "plans": "...",
  "risk_score": 3,
  "risk_feedback": "...",
  "Warnings": "...",
  "final_score": 8,
  "final_feedback": "...",
  "recommendations": "..."
}
```

---

## Programmatic Usage

```python
from graph import app as graph_app

initial_state = {
    "user_prompt": "Plan a 7-day adventure trip to Iceland with $5000 budget"
}

result = graph_app.invoke(initial_state)
print(f"Final Score: {result['final_score']}/10")
print(f"Recommendations: {result['recommendations']}")
```

---

## Key Implementation Details

### Parallel Execution
The graph executes three analysis nodes **concurrently**, not sequentially:
- Traditional sequential: ~9-12 seconds (3 LLM calls × 3-4 seconds each)
- Parallel execution: ~3-4 seconds (3 concurrent LLM calls)

### Structured Outputs
All nodes use Pydantic models with `.with_structured_output()` to guarantee:
- Type-safe responses
- No JSON parsing errors
- Schema validation
- Predictable data structures

### State Management
Each node returns only the fields it produces. LangGraph automatically merges these into the shared state, making all data available to downstream nodes.

---

## Advantages of This Pattern

1. **Performance** - Parallel execution reduces total latency
2. **Modularity** - Each analysis type is isolated and independently testable
3. **Type Safety** - Pydantic models prevent runtime errors
4. **Scalability** - Easy to add more parallel analysis nodes
5. **Maintainability** - Clear separation of concerns

---

## Possible Enhancements

- Add request validation using Pydantic models in FastAPI endpoint
- Implement retry logic for LLM failures
- Add caching for common queries
- Create a `requirements.txt` file
- Add unit tests for each node function
- Implement streaming responses for real-time updates
- Add more parallel nodes (weather analysis, local events, etc.)

---

## Comparison: Sequential vs Parallel

| Aspect | Sequential (previous example) | Parallel (this example) |
|--------|------------------------------|-------------------------|
| Execution | One node at a time | Multiple nodes simultaneously |
| Latency | Sum of all node times | Max of any single node time |
| Use Case | Steps depend on previous results | Independent analyses |
| Example | Outline → Blog → Evaluation | Budget + Itinerary + Risk |

---

## Notes

- Typo in code: "Budject" should be "Budget" (kept as-is for consistency with existing code)
- The `final_node` only uses 3 of the 9 available state fields for synthesis
- All LLM calls use `temperature=0` for consistent, deterministic outputs
- The FastAPI endpoint accepts `user_prompt` as a query parameter (consider switching to JSON body for production)

---

**Ready to use!** Start the server and send travel planning queries to see parallel execution in action.
