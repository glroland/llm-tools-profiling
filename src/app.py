import os
import logging
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

logger = logging.getLogger('langchain.agents.agent')
logger.disabled = True

TOGETHER_ENDPOINT = "https://api.together.xyz/v1"
TOGETHER_TOKEN = os.environ["TOGETHER_API_KEY"]
TOGETHER_MODELS = [
]
OPENAI_MODELS = [
    "gpt-3.5-turbo"
]

was_multiply_invoked = False

@tool
def multiply(a: int, b: int) -> int:
    """ Multiply two numbers together. """
    global was_multiply_invoked
    was_multiply_invoked = True
    result = a * b
    #print (f"Multiplying {a} * {b}.  The answer is {result}")
    return result

def test_model(endpoint, token, model_name):
    global was_multiply_invoked
    was_multiply_invoked = False

    llm = ChatOpenAI(base_url=endpoint,
                    api_key=token,
                    model=model_name,
                    temperature=0.7)

    system_prompt = """You are a helpful assistant.  Use the tools provided to respond to user queries accurately and kindly."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    tools = [multiply]
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
    )

    response = agent_executor.invoke({"input": "What's 8 * 4?"})
    output = response["output"]

    if was_multiply_invoked:
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")


for model in OPENAI_MODELS:
    print (f"Testing OpenAI Model: {model}")
    print ("----------------------------------------")
    test_model(None, None, model)
    print ()

for model in TOGETHER_MODELS:
    print (f"Testing Together Model: {model}")
    print ("----------------------------------------")
    test_model(TOGETHER_ENDPOINT, TOGETHER_TOKEN, model)
    print ()
