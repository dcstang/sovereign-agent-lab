"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Albanach"
QUERY_1_VENUE_ADDRESS = "2 Hunter Square, Edinburgh"
QUERY_2_FINAL_ANSWER  = (
    "No venue is available in the database that can accommodate 300 people "
    "with vegan options. The largest vegan-friendly available venue is "
    "The Albanach (capacity 180), which does not meet the 300-person requirement."
)

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Changed The Albanach's status from 'available' to 'full' in mcp_venue_server.py,
then re-ran exercise4_mcp_client.py. The search_venues tool now returned only
The Haymarket Vaults for Query 1 (160 guests, vegan), because The Albanach was
filtered out by the status check. The agent client code (exercise4_mcp_client.py)
did not need any changes — it discovers tools dynamically and calls them unchanged.
Only mcp_venue_server.py needed updating. This demonstrates the core MCP value:
data and logic live in one place; all connected clients immediately reflect the change.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 225   # sovereign_agent/tools/venue_tools.py (hardcoded @tool functions)
LINES_OF_TOOL_CODE_EX4 = 30    # _make_mcp_caller + discover_tools bridge in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP provides a standard protocol so any compatible client — a LangGraph agent,
a Rasa action, a CLI script — can connect to the same server and discover tools
dynamically at runtime without code changes. Tools are versioned and deployed
independently of the agents that use them. Adding a new @mcp.tool() to the server
is immediately visible to every connected client without redeployment or import
changes. This language- and framework-agnostic contract is what separates MCP
from simply moving functions into a shared module.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
- The LangGraph research agent acts as the autonomous reasoning loop because it
  can plan multi-step tool calls, recover from tool errors, and decide when it has
  gathered enough information — all without step-by-step human instruction.
- The MCP venue server centralises all venue data and business logic so that any
  client (Rasa, LangGraph, CLI) gets a consistent, up-to-date view without code
  duplication across the codebase.
- The Rasa CALM dialogue manager handles real-time voice/text conversation with
  the customer because it enforces structured flows (greeting, slot-filling,
  confirmation) that are too rigid for a free-form LLM loop.
- A persistent memory store (e.g. Redis or a SQL database) retains booking state
  across turns and sessions so the agent can resume interrupted conversations and
  avoid asking the user for information already provided.
- An orchestrator layer routes incoming requests to either the research agent or
  the Rasa dialogue manager based on intent, ensuring each component handles only
  the task it is designed for and preventing the agents from being swapped into
  roles they perform poorly.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
The LangGraph ReAct agent should handle research because, as observed in exercise 4,
it autonomously chains tool calls (search_venues then get_venue_details) and adapts
its plan based on results — for example correctly reporting no match for 300 guests
without hallucinating a venue. The Rasa CALM agent should handle the confirmation
call because it enforces a predictable slot-filling flow (name, date, guest count,
vegan requirement) that users expect in a booking conversation.

Swapping feels wrong for two concrete reasons observed in the runs: the LangGraph
agent produces raw JSON-style function-call output (as seen in the printed trace)
rather than natural dialogue, which would be jarring in a live phone call; and the
Rasa flows.yml described in exercise 2 task D is explicit and auditable, ensuring
no step is skipped — the free-form LLM loop in LangGraph could skip confirmation
or misinterpret a vague user response, a critical failure in a booking scenario.
"""
