import os
import logging
from tests import test_model

TOGETHER_ENDPOINT = "https://api.together.xyz/v1"
TOGETHER_TOKEN = os.environ["TOGETHER_API_KEY"]
TOGETHER_MODELS = [
    # Fails on everything
    # "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    # "Qwen/Qwen2.5-VL-72B-Instruct",
    # "mistralai/Mixtral-8x7B-Instruct-v0.1"
    # "meta-llama/Llama-3-8b-chat-hf"
    #"meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"

    # Failing on most tests
    # "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"

    # Failing on some tests
    #"meta-llama/Llama-4-Scout-17B-16E-Instruct",
    #"deepseek-ai/DeepSeek-R1",

    # Failing only on chained, sequential calls where output of one is fed into another
    #"meta-llama/Llama-3.3-70B-Instruct-Turbo",
    #"mistralai/Mistral-Small-24B-Instruct-2501"
    #"nvidia/Llama-3.1-Nemotron-70B-Instruct-HF"

    # Doesn't finish 4, passes first 3
    #"Qwen/Qwen3-235B-A22B-fp8-tput",

    # Successful with all tests
    #"deepseek-ai/DeepSeek-V3",

]
OPENAI_MODELS = [
    # Successful with all tests
    #"gpt-3.5-turbo",
]

def main():
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

if __name__ == "__main__":
    main()