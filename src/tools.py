from langchain_core.tools import tool

was_multiply_invoked = False
was_get_age_invoked = False

def was_tool_invoked(tool: str) -> bool:
    global was_multiply_invoked
    global was_get_age_invoked

    if tool == "multiply":
        return was_multiply_invoked
    elif tool == "get_age":
        return was_get_age_invoked
    raise ValueError(f"Unknown tool: {tool}")

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

def reset():
    global was_multiply_invoked
    was_multiply_invoked = False
    global was_get_age_invoked
    was_get_age_invoked = False

TOOLS = [multiply, get_age]
