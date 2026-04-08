"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = (
    "The model (Llama 3.3 70B) did not emit proper tool-use signals — it output all five "
    "tool calls as raw JSON text inside a single AI message rather than triggering the "
    "LangGraph tool node. As a result, tool_calls_made was empty and no tools actually ran. "
    "The weather outdoor_ok=False value is taken from Scenario 1 (Task C), where the weather "
    "tool did execute and returned outdoor_ok: false, temp 8.9°C, precipitation 0.2mm."
)

# ── Task B ─────────────────────────────────────────────────────────────────

# Has generate_event_flyer been implemented (not just the stub)?
TASK_B_IMPLEMENTED = True   # True or False

# The image URL returned (or the error message if still a stub).
TASK_B_IMAGE_URL_OR_ERROR = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-a5f9524e-ce0c-4a53-8dad-5cb905ebc520_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for AI Meetup, professional, Scottish at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The pivot is visible in the tool results: The Bow Bar returned meets_all_constraints: false
(capacity 80, status full), so the agent immediately moved on and called check_pub_availability
for The Haymarket Vaults next, which returned meets_all_constraints: true. Without any
instruction to do so, the agent recognised the first venue failed and switched to another
from the known list — a clean, unprompted fallback driven purely by the tool result.
"""

SCENARIO_1_FALLBACK_VENUE = "The Haymarket Vaults"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the known venues meet the capacity and dietary requirements. The Albanach, The Haymarket
Vaults, and The Guilford Arms have a capacity of 180, 160, and 200 respectively, which is less
than the required capacity of 300. The Bow Bar has a capacity of 80, which is also less than the
required capacity, and it is currently full. Therefore, none of the known venues can accommodate
300 people with vegan options.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = "Your input is lacking necessary details. Please provide more information or specify the task you need help with."

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
The behaviour is partially acceptable but not ideal. The agent correctly avoided calling any tool
and did not hallucinate train schedule data — both good outcomes. However, the response
("Your input is lacking necessary details") is confusing and unhelpful to a real user. A
production booking assistant should instead respond with a clear, polite explanation that train
times are outside its scope and suggest the user try a service like National Rail. Avoiding
hallucination is correct; the poor phrasing of the refusal is the failure point here.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/rules.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph graph has just three nodes — agent, tools, and end — connected in a tight
reasoning loop. The agent decides at runtime which tools to call and in what order; there are
no named intents or explicit paths. Rasa CALM's flows.yml, by contrast, describes every
conversational task as a named flow with discrete steps: the structure is explicit, authored
upfront, and the LLM's job is to pick the right flow rather than to reason freely about the
next action. LangGraph is open-ended and dynamic; Rasa CALM is structured and auditable.
Both approaches have value — CALM is easier to constrain and test; LangGraph is more flexible
but harder to guarantee correct behaviour.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most surprising behaviour was in Task A: the model (Llama 3.3 70B) output all five tool
calls as raw JSON text inside a single AI message instead of triggering the LangGraph tool
node. This meant no tools actually executed — tool_calls_made was empty — yet the agent
reported "success: true". The model understood the task perfectly and even selected the right
tool arguments, but it serialised the calls as plain text rather than emitting proper
function-call tokens. This is a stark reminder that LangGraph's tool loop depends entirely on
the underlying model supporting the tool-calling protocol correctly; a capable model that talks
about tools but does not use them is effectively broken in an agentic context.
"""
