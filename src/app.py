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
#    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
#    "meta-llama/Llama-3.3-70B-Instruct-Turbo",
#    "Qwen/Qwen2.5-VL-72B-Instruct",
#    "meta-llama/Llama-4-Scout-17B-16E-Instruct",
]
OPENAI_MODELS = [
    "gpt-3.5-turbo",
]

was_multiply_invoked = False
was_get_age_invoked = False

@tool
def multiply(a: int, b: int) -> int:
    """ Multiply two numbers together. """
    global was_multiply_invoked
    was_multiply_invoked = True
    result = a * b
    #print (f"Multiplying {a} * {b}.  The answer is {result}")
    return result

@tool
def get_age(name: str) -> int:
    """ Get the age of the person identified by name. """
    global was_get_age_invoked
    was_get_age_invoked = True
    ages = [
        {'name': 'bob', 'age': 52},
        {'name': 'jane', 'age': 25},
        {'name': 'john', 'age': 42}
    ]
    for person in ages:
        if person["name"].lower() == name.lower():
            return int(person["age"])
    raise ValueError("Cannot find person with name: " + name)

system_prompt = """You are a helpful assistant.  When relevant to the user's inquiry, use the tools provided to accurately respond to user queries.  """
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def reset():
    global was_multiply_invoked
    was_multiply_invoked = False
    global was_get_age_invoked
    was_get_age_invoked = False

def run_test(llm, test_prompt):
    tools = [multiply, get_age]

    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
    )

    response = agent_executor.invoke({"input": test_prompt})
    output = response["output"]
    return output

def test_model(endpoint, token, model_name):
    reset()

    llm = ChatOpenAI(base_url=endpoint,
                    api_key=token,
                    model=model_name,
                    temperature=0.7)

    output = run_test(llm, "What's the capital of France?")
    if not was_multiply_invoked and not was_get_age_invoked:
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

    output = run_test(llm, "Bob's favorite number is 4.  What is 8 times that number?")
    if was_multiply_invoked and not was_get_age_invoked:
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

    output = run_test(llm, "What is Bob's age times two?")
    if was_multiply_invoked and was_get_age_invoked:
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}. Mult={was_multiply_invoked} Age={was_get_age_invoked}")


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
