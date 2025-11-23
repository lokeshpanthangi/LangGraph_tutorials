**Overview**
- **Description:** This folder contains a small sequential state-graph example that builds a simple blog-generation pipeline. The pipeline takes a `user_prompt`, generates an outline, writes a blog post from the outline, and evaluates the blog with a score and feedback.

**Files**
- `graph.py`: Assembles a `StateGraph` using `State` and three node functions: `outline_gen`, `blog_gen`, and `blog_evaluator`.
- `main.py`: A tiny `FastAPI` app exposing two endpoints: `/healthy` and `/GenerateBlogPost`. It invokes the compiled graph to process incoming prompts.
- `nodes.py`: Implements the three pipeline node functions that call an LLM model to produce an outline, generate a blog, and evaluate the blog. It uses `langchain_openai.ChatOpenAI` and `python-dotenv`.
- `state.py`: Defines a `TypedDict` `State` describing the shape of the state passed between nodes.

**Design / Flow**
- Input: a `user_prompt` string provided to the HTTP endpoint.
- Step 1 (`Outline Generation`): create a detailed outline for the requested blog post.
- Step 2 (`Blog Generation`): write the blog post using the outline.
- Step 3 (`Blog Evaluation`): evaluate the generated blog against the outline and return a numeric `score` and textual `feedback`.

**Requirements**
- Python 3.9+ recommended
- Suggested packages (install with `pip`): `fastapi`, `uvicorn`, `python-dotenv`, `langchain-openai` (or the specific LLM wrapper you use).

Example install command (PowerShell):

```powershell
pip install fastapi uvicorn python-dotenv langchain-openai
```

You must set your LLM / OpenAI credentials in the environment (for example via a `.env` file or environment variables). `nodes.py` calls `load_dotenv()` so a `.env` file in the project root is supported.

**Running the service (development)**
- Start the FastAPI app (from this folder) with Uvicorn:

```powershell
#$env:OPENAI_API_KEY = "your_openai_key_here"  # (optional) set in session
uvicorn main:app --reload
```

**HTTP API**
- `POST /healthy` — simple health-check that returns `{ "status": "healthy" }`.
- `POST /GenerateBlogPost` — invokes the graph pipeline. The endpoint expects a `user_prompt` string parameter. Example (using query parameter):

```bash
curl -X POST "http://127.0.0.1:8000/GenerateBlogPost?user_prompt=Write%20a%20blog%20about%20AI%20in%20education"
```

Response: the final state dictionary with at least these keys: `user_prompt`, `outline`, `blog`, `score`, `feedback`.

**Example usage (programmatic)**
- The graph is assembled in `graph.py` using `StateGraph(State)` and node functions from `nodes.py`. The compiled graph exposes an `invoke(initial_state)` method that accepts the `State` dict and returns the updated `State` after running all nodes in order.

Minimal example (same logic as `main.py`):

```python
from graph import app as graph_app

initial_state = {
	"user_prompt": "Write a tutorial-style blog about prompt engineering",
	"outline": "",
	"blog": "",
	"score": 0,
	"feedback": ""
}

final_state = graph_app.invoke(initial_state)
print(final_state)
```

**Implementation notes & considerations**
- `nodes.py` uses `langchain_openai.ChatOpenAI` with `model_name="gpt-4o-mini"` and `temperature=0`. Adjust model name, temperature, or client configuration according to your account and SDK version.
- `blog_evaluator` expects the LLM to return a JSON string with keys `score` and `feedback`; the code uses `json.loads` to parse the response. Ensure the model prompt enforces strict JSON formatting to avoid parsing errors.
- The endpoint signature in `main.py` currently accepts `user_prompt: str` as a parameter — when calling via HTTP you can pass it as a query parameter (shown above) or modify the endpoint to accept a JSON body/Pydantic model for more robust usage.

**Next steps / improvements**
- Add input validation (Pydantic models) to the `FastAPI` endpoint.
- Add retry/error handling around LLM calls and JSON parsing.
- Provide a small test harness or example `.env` template (`.env.example`) documenting required variables.
- Add a `requirements.txt` or `pyproject.toml` to lock dependencies.

If you want, I can also:
- create a `requirements.txt` and `.env.example`,
- convert the endpoint to accept JSON body payloads,
- or add a small tests/example script to exercise the pipeline.

