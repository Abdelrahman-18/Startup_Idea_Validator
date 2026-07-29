#prompts, parsers,chains , chat 

import re
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from core.models import BusinessAnalysis, SWOTAnalysis, InvestmentReadiness
from core.rag import retrieve_context


# Parsers
business_parser = PydanticOutputParser(pydantic_object=BusinessAnalysis)
swot_parser = PydanticOutputParser(pydantic_object=SWOTAnalysis)
investment_parser = PydanticOutputParser(pydantic_object=InvestmentReadiness)


# Prompts
business_prompt = ChatPromptTemplate.from_template(
    """You are a senior startup analyst. Analyze the startup using ONLY the context below.
Do not invent facts that are not supported by the context.

Context:
{context}

Task:
Extract the core business details of this startup.

{format_instructions}

Respond with ONLY the JSON object. No extra text, no markdown code fences."""
)

swot_prompt = ChatPromptTemplate.from_template(
    """You are a senior startup analyst. Perform a SWOT analysis using ONLY the context below.

Context:
{context}

Task:
Identify Strengths, Weaknesses, Opportunities, and Threats for this startup.
Each list should have 2-5 concise items.

Respond with ONLY a JSON object in exactly this shape, with no extra nesting:

{{
  "strengths": ["item 1", "item 2"],
  "weaknesses": ["item 1", "item 2"],
  "opportunities": ["item 1", "item 2"],
  "threats": ["item 1", "item 2"]
}}

No extra text, no markdown code fences, no schema, no "properties" key, just the flat JSON object above filled in with real content."""
)

investment_prompt = ChatPromptTemplate.from_template(
    """You are a venture capital analyst. Evaluate investment readiness using ONLY the context below.

Context:
{context}

Task:
Score this startup's investment readiness from 0-100 and justify the score.
Be honest and critical -- do not inflate the score if information is missing.

{format_instructions}

Respond with ONLY the JSON object. No extra text, no markdown code fences."""
)

RETRIEVAL_QUERIES = {
    "business": "business model, problem, solution, target customers, value proposition, revenue",
    "swot": "strengths weaknesses opportunities threats competition risks advantages",
    "investment": "team traction scalability market size funding financials risks growth",
}


# generation and parsing
def generate_text(chat_model, prompt: str) -> str:
    return chat_model.invoke(prompt).content


def unwrap_schema_echo(data: dict) -> dict:
    """If the model echoed the schema's own shape instead of a flat
    instance, pull the real values back out into a flat dict."""
    if not isinstance(data, dict) or "properties" not in data:
        return data
    unwrapped = {}
    for key, val in data["properties"].items():
        if isinstance(val, dict) and "items" in val:
            unwrapped[key] = val["items"]
        elif isinstance(val, dict) and "value" in val:
            unwrapped[key] = val["value"]
        else:
            unwrapped[key] = val
    return unwrapped


def safe_parse(raw_output: str, parser: PydanticOutputParser):
    matches = re.findall(r"\{.*\}", raw_output, re.DOTALL)
    candidate = matches[-1] if matches else raw_output

    try:
        return parser.parse(candidate)
    except Exception:
        try:
            data = json.loads(candidate)
            data = unwrap_schema_echo(data)
            return parser.pydantic_object.model_validate(data)
        except Exception as e:
            raise RuntimeError(f"Could not parse model output: {e}\n\nRaw output:\n{raw_output}")


def run_chain(chat_model, prompt: ChatPromptTemplate, parser: PydanticOutputParser, context: str):
    format_vars = {"context": context}
    if "format_instructions" in prompt.input_variables:
        format_vars["format_instructions"] = parser.get_format_instructions()
    formatted = prompt.format(**format_vars)
    raw = generate_text(chat_model, formatted)
    return safe_parse(raw, parser)



# Chat with memory
def generate_chat_answer(chat_model, retriever, question: str, chat_history: list) -> str:
    context, _ = retrieve_context(retriever, question)

    history_text = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in chat_history
    )

    prompt = f"""You are an AI assistant answering questions about a startup document.
Use the conversation history for continuity and the context for facts. If the context
doesn't contain the answer, say so honestly instead of guessing.

Conversation history:
{history_text}

Context from document:
{context}

Question: {question}
Answer:"""

    return generate_text(chat_model, prompt)
