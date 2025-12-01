# Interview Questions for MoveInSync Project

This document contains a list of technical interview questions based on the analysis of your MoveInSync backend and AI agent project. The questions are categorized to help you prepare for different aspects of the interview.

## 1. Architecture & System Design

1.  **Can you explain the high-level architecture of your application?**
    *   *Focus on the separation between the FastAPI backend and the LangGraph agent.*
2.  **Why did you choose FastAPI for this project?**
    *   *Discuss async capabilities, automatic docs, and performance.*
3.  **How does the AI agent integrate with the rest of the backend?**
    *   *Explain the `/movi/chat` endpoint and how it invokes the graph.*
4.  **What is the purpose of the `Agents` directory structure?**
    *   *Explain the roles of `graph.py`, `nodes.py`, `state.py`, and `tools.py`.*
5.  **How do you handle state management in your AI agent?**
    *   *Discuss the `MoviState` TypedDict and what information it persists.*
6.  **Why did you choose LangGraph over a standard LangChain agent?**
    *   *Mention control flow, cycles, and specifically the `interrupt` mechanism for HITL.*
7.  **How does your system handle concurrent users?**
    *   *Discuss `thread_id` in the config and how FastAPI handles async requests.*
8.  **What design pattern is used for the database connections?**
    *   *Explain the `SessionLocal` and dependency injection pattern (`get_db`).*

## 2. LangGraph & Agent Logic

9.  **Walk me through the flow of a single user message through your agent graph.**
    *   *Trace: Intent -> Consequence -> Tool Call -> Response.*
10. **How does the `intent_node` work?**
    *   *Explain how it uses the LLM to classify intent and extract entities.*
11. **What is the purpose of the `consequence_node`?**
    *   *Explain the check for high-impact tools and the `interrupt` mechanism.*
12. **How specifically do you implement "Human-in-the-Loop" (HITL)?**
    *   *Detail the use of `interrupt`, `Command(resume=...)`, and how the API handles the `confirmation` event.*
13. **How does the agent know which tools are available?**
    *   *Explain the `get_tools_for_page` logic and why context-awareness is important.*
14. **What happens if the LLM hallucinates a tool name?**
    *   *Look at the `tool_call_node` error handling logic.*
15. **How do you handle entity extraction and normalization?**
    *   *Discuss how `tool_call_node` maps "trip_name" to "trip_display_name".*
16. **What is the role of the `response_node`?**
    *   *Explain how it synthesizes the final answer from tool results and history.*

## 3. Backend & API (FastAPI)

17. **How is the `/movi/chat` endpoint implemented to support streaming?**
    *   *Discuss `StreamingResponse`, NDJSON format, and `astream_events`.*
18. **What are the different event types returned by your chat stream?**
    *   *Mention `token`, `confirmation`, and `error`.*
19. **How do you handle the "resume" action when a user confirms a high-impact action?**
    *   *Explain the `state.next` check and `Command(resume=user_approved)`.*
20. **How is the LiveKit token generation implemented?**
    *   *Explain the `/voice/token` endpoint and the grants provided.*
21. **How do you handle dependency injection for the database session?**
    *   *Explain `Depends(get_db)` (even though the agent uses `SessionLocal` directly - be ready to explain why).*
22. **What is the purpose of the `CORSMiddleware` configuration in `main.py`?**
    *   *Explain why `allow_origins=["*"]` is used (dev vs prod).*
23. **How are the routers organized in your application?**
    *   *Discuss `app.include_router` and the modular structure in `routes/`.*

## 4. Database & Tools

24. **How do your tools interact with the database?**
    *   *Explain the pattern: Tool -> CRUD function -> DB Query.*
25. **What is the difference between `flush()` and `commit()` in your `create_new_stop` tool?**
    *   *Explain why `flush` is used for bulk creation to get IDs before committing.*
26. **How do you ensure data integrity when deleting a trip?**
    *   *Explain the check for deployments and how they are handled before deleting the trip.*
27. **How does the `check_trip_consequences` function work?**
    *   *Explain the logic for checking booking percentages and generating warnings.*
28. **What is the purpose of the `HIGH_IMPACT_TOOLS` set?**
    *   *Explain how it acts as a filter for the consequence node.*
29. **How do you handle complex queries, like finding unassigned vehicles?**
    *   *Explain the `NOT IN` query logic in `get_unassigned_vehicles`.*
30. **How are the database models defined?**
    *   *Briefly mention SQLAlchemy `Base` and relationships (e.g., `Trip` -> `Deployment`).*

## 5. Advanced Features (Vision & AI)

31. **How does your agent handle image inputs?**
    *   *Explain the vision capabilities in `intent_node` using GPT-4o.*
32. **How do you optimize the context window when handling images?**
    *   *Mention replacing the base64 image with a text description in the state.*
33. **How does the system prompt change when an image is present?**
    *   *Discuss the specific instructions for highlighted/circled items.*
34. **How do you generate the AI alert for confirmation messages?**
    *   *Explain the secondary LLM call in `/movi/chat` to generate a natural language warning.*
35. **What model are you using for the main agent vs. the vision task?**
    *   *GPT-4o-mini vs GPT-4o and why.*
36. **How would you scale this agent to handle more complex workflows?**
    *   *Discuss subgraphs or multi-agent architectures.*

## 6. Scenario-Based Questions

37. **If I wanted to add a new tool for "Driver Analytics", what steps would I need to take?**
    *   *Define tool -> Add to list -> Update CRUD/DB -> Test.*
38. **How would you debug a situation where the agent is stuck in a loop?**
    *   *Discuss checking the `recursion_limit` or state updates.*
39. **The user reports that the agent "forgot" what they said 5 messages ago. How would you investigate?**
    *   *Check the message history limit (10 messages) in `movi.py`.*
40. **How would you secure the `delete_trip` tool so only admins can use it?**
    *   *Discuss adding a "role" field to the state or user context.*
