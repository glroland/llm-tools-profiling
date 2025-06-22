from pydantic_core._pydantic_core import ValidationError
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import TOOLS, reset, was_tool_invoked

def test_model(endpoint, token, model_name):
    reset()

    llm = ChatOpenAI(base_url=endpoint,
                    api_key=token,
                    model=model_name,
                    temperature=0.7)

    run_all_tests(llm)

def run_test(llm, test_prompt):
    tools = TOOLS

    system_prompt = """You are a helpful assistant.  When relevant to the user's inquiry, use the tools provided to accurately respond to user queries.  The use of tools is optional if you can confidently answer the question based on your own knowledge. """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
    )

    try:
        response = agent_executor.invoke({"input": test_prompt})
        output = response["output"]
        return output
    except ValidationError as e:
        return "EXCEPTION::ValidationError::" + str(e)
    except ValueError as e:
        return "EXCEPTION::ValueError::" + str(e)

def run_all_tests(llm):
    run_test_no_tools(llm)
    run_test_one_tool(llm)
    run_test_two_tools_parallel(llm)
    run_test_two_tools_dependence(llm)
    run_test_many_tools_dependence(llm)

def run_test_no_tools(llm):
    output = run_test(llm, "What's the capital of France?")
    if not was_tool_invoked("multiply") and \
       not was_tool_invoked("get_age") and \
       "PARIS" in output.upper():
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

def run_test_one_tool(llm):
    output = run_test(llm, "Bob's favorite number is 4.  What is 8 times that number?")
    if was_tool_invoked("multiply") and \
       not was_tool_invoked("get_age") and \
       "32" in output.upper():
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

def run_test_two_tools_parallel(llm):
    output = run_test(llm, "What is Bob's age?  What is 5 * 9?")
    if was_tool_invoked("multiply") and \
       was_tool_invoked("get_age") and \
       "52" in output.upper() and \
       "45" in output.upper():
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

def run_test_two_tools_dependence(llm):
    output = run_test(llm, "What is Bob's age times two?")
    if was_tool_invoked("multiply") and \
       was_tool_invoked("get_age") and \
       "104" in output.upper():
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")

def run_test_many_tools_dependence(llm):
    output = run_test(llm, "What is Bob's age times Jane's age times John's age times 4?")
    if was_tool_invoked("multiply") and \
       was_tool_invoked("get_age") and \
       "218400" in output.upper():
        print (f"PASSED!!!  {output}")
    else:
        print (f"FAILED!!!  {output}")
