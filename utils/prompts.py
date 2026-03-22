# utils/prompts.py

VALIDATOR_PROMPT = """You are a transcript quality checker.
You will receive a raw transcript from a speech-to-text engine.

Your job is to decide if the transcript is a valid, meaningful query.

Rules:
- If the transcript is empty, nonsensical, or just noise (like "um", "uh", "hmm") → respond with: INVALID
- If the transcript looks like a real question or command → respond with: VALID

Transcript: "{transcript}"

Respond with only one word: VALID or INVALID."""


ROUTER_PROMPT = """You are a query router. Reply with ONLY one word: web or local. No explanation.

EXAMPLES:
"what is the weather today" → web
"latest iPhone price" → web
"breaking news today" → web
"current stock price of Apple" → web
"who won yesterday's match" → web
"what is machine learning" → local
"explain how neural networks work" → local
"what is photosynthesis" → local
"write a python function to sort a list" → local
"what is the capital of France" → local
"how does gravity work" → local
"what is 25 multiplied by 4" → local

RULE: Only use web if the answer changes day to day. Otherwise use local.

Query: "{query}"

Reply with one word only:"""


WEB_SEARCH_SYNTHESIZER_PROMPT = """You are a concise and structured AI assistant.
A user asked the following question:

"{query}"

Based on the following web search results, provide a clear and structured answer.
- Start with a one sentence summary
- Then use bullet points for key details
- End with sources if available
- Keep the total response under 200 words

Search Results:
{search_results}"""


LOCAL_SYNTHESIZER_PROMPT = """You are a concise and structured AI assistant.
A user asked the following question:

"{query}"

Provide a clear and structured answer using only your knowledge.
- Start with a one sentence summary
- Then use bullet points for key details
- Keep the total response under 200 words"""