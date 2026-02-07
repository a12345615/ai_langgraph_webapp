import os
from typing import TypedDict, List, Literal, Optional

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from prompts import SYSTEM_PROMPT, ROUTER_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-70b")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY. Put it in .env")

llm = ChatGroq(model=MODEL_NAME, api_key=GROQ_API_KEY)

Intent = Literal["general", "code"]

class State(TypedDict):
    user_input: str
    intent: Intent
    answer: str
    history: List[dict]  # [{role: "user"/"assistant", content: "..."}]

def _history_to_messages(history: List[dict]):
    msgs = []
    for item in history[-10:]:  # keep last 10 turns
        role = item.get("role")
        content = item.get("content", "")
        if role == "user":
            msgs.append(HumanMessage(content=content))
        elif role == "assistant":
            msgs.append(AIMessage(content=content))
    return msgs


class _DummyResp:
    def __init__(self, content: str):
        self.content = content


def safe_invoke(messages):
    try:
        return llm.invoke(messages)
    except Exception as e:
        # Return a dummy response object with an error message
        err = f"LLM invocation error: {e}"
        print(err)
        return _DummyResp(err)

def route_intent(state: State) -> State:
    user_input = state["user_input"]
    resp = safe_invoke([
        SystemMessage(content=ROUTER_PROMPT),
        HumanMessage(content=user_input),
    ])
    text = (resp.content or "").strip().lower()
    intent: Intent = "code" if text == "code" or "code" in text else "general"
    return {**state, "intent": intent}

def general_node(state: State) -> State:
    user_input = state["user_input"]
    history = state.get("history", [])

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages += _history_to_messages(history)
    messages += [HumanMessage(content=user_input)]

    resp = safe_invoke(messages)
    answer = resp.content or ""

    new_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": answer},
    ]

    return {**state, "answer": answer, "history": new_history}

def code_node(state: State) -> State:
    user_input = state["user_input"]
    history = state.get("history", [])

    code_system = SYSTEM_PROMPT + """
When you provide code:
- keep it minimal and runnable
- include brief comments
- if environment assumptions exist, state them in 1 line
"""

    messages = [SystemMessage(content=code_system)]
    messages += _history_to_messages(history)
    messages += [HumanMessage(content=user_input)]

    resp = safe_invoke(messages)
    answer = resp.content or ""

    new_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": answer},
    ]

    return {**state, "answer": answer, "history": new_history}

def choose_path(state: State) -> str:
    return "code_node" if state["intent"] == "code" else "general_node"

def build_graph():
    g = StateGraph(State)

    g.add_node("route_intent", route_intent)
    g.add_node("general_node", general_node)
    g.add_node("code_node", code_node)

    g.set_entry_point("route_intent")
    g.add_conditional_edges("route_intent", choose_path, {
        "general_node": "general_node",
        "code_node": "code_node",
    })

    g.add_edge("general_node", END)
    g.add_edge("code_node", END)

    return g.compile()

graph_app = build_graph()
