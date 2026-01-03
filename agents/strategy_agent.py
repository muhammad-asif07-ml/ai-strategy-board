from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from state.shared_state import StrategyState



prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the CEO synthesizing board opinions."),
    ("human", "{opinions}")
])

def strategy_agent(state: StrategyState) -> StrategyState:
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    opinions_text = "\n\n".join(
        f"{op.agent}: {op.opinion}" for op in state.board_opinions
    )

    response = llm.invoke(prompt.format(opinions=opinions_text))

    return state.copy(update={
        "final_recommendation": response.content,
        "history": state.history + [{"agent": "CEO", "output": response.content}]
    })
