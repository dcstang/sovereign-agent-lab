"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you expecting tonight?
Your input ->  160 guests
How many guests will require vegan meals?
Your input ->  about 50 need vegan
What deposit amount (in GBP) are you proposing?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals,
£200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you expecting tonight?
Your input ->  160 guests
How many guests will require vegan meals?
Your input ->  about 50 need vegan
What deposit amount (in GBP) are you proposing?
Your input ->  £500 deposit
I need to check one thing with the organiser before I can confirm.
The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300.
Can I call you back within 15 minutes?
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  calling to confirm a booking
How many guests are you expecting tonight?
Your input ->  160 guests
How many guests will require vegan meals?
Your input ->  can you arrange parking for the speakers?
I'm sorry, arranging parking is outside the scope of what I can help with
during a booking confirmation call. Could you tell me how many guests
will require vegan meals tonight?
Your input ->  about 50 need vegan
What deposit amount (in GBP) are you proposing?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals,
£200 deposit accepted. I'll send written confirmation to the organiser shortly.
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM recognised the parking question as outside the booking confirmation scope,
triggered the handle_out_of_scope flow which delivered a polite deflection message,
and then seamlessly returned to the confirm_booking flow to continue collecting
the vegan count where it left off.
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
LangGraph's research agent in Exercise 2 tried to be helpful with the out-of-scope
request — it would attempt to use its tools or reason through an answer because the
LLM had full discretion over every step. Rasa CALM, by contrast, has an explicit
handle_out_of_scope flow defined in flows.yml. The LLM's only job is to recognise
the request is off-topic and route to that pre-written deflection. CALM cannot
improvise a helpful answer; it can only deliver the scripted response. This is more
predictable and auditable but less flexible than the LangGraph approach.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
After uncommenting the four lines in the TASK B block in actions.py and retraining
with `make ex3-retrain`, I temporarily changed the condition to `if True:` so it
would always fire regardless of the actual clock time. I then ran a booking
conversation and verified the agent immediately escalated with the message
"it is past 16:45 — insufficient time to process the confirmation before the
5 PM deadline". I then reverted the condition back to the real time check.
At the natural test time (approaching 16:45), the agent correctly checked
the time difference and escalated the booking confirming the guard works as intended.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
CALM gains significant simplicity by eliminating the ValidateBookingConfirmationForm
class and all the regex parsing code that old Rasa required. The LLM now handles
slot extraction via `from_llm` mappings — "about 160 people", "one-sixty", and
"we're expecting 160" all become 160.0 without any Python on our side.

Python still handles the business rules in ActionValidateBooking, and for good reason:
these are deterministic, financially binding constraints (MAX_DEPOSIT_GBP = 300,
MAX_GUESTS = 170). The LLM cannot negotiate them away or misinterpret them.
One might trust the old approach more for the slot-extraction step — regex is
transparent and predictable, whereas the LLM could in theory misparse an edge case.
The trade-off is that regex is brittle to natural phrasing variation while the LLM
handles it gracefully.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The considerable setup cost of CALM (config.yml, domain.yml, flows.yml, endpoints.yml,
rasa train, two terminals, Rasa Pro licence) buys you predictability and auditability.
Every possible conversation path is explicitly declared in flows.yml — you can read
exactly what the agent will do in any situation. The agent CANNOT improvise a response
it wasn't trained on, and it CANNOT call a tool that wasn't defined in flows.yml.
For the booking confirmation use case, this is a feature, not a limitation: you want
a deterministic agent that always collects the same three slots and always applies
the same business rules. You do NOT want the agent improvising creative alternatives
to Rod's deposit limit. LangGraph could improvise — which made it powerful for the
research use case but would be a liability here where every decision has financial
and legal consequences.
"""
