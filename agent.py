from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
import os
load_dotenv()
client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  # required but ignored
)

def get_weather(city: str): #weather api calling logic
    url = f"https://wttr.in/{city}?format=%C+%t" #open source weather api, we don't need to create apis for weather
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    
    return "Something went wrong"

def run_command(cmd: str): #executing system commands logic
    result = os.system(cmd)
    return result

def get_stock_price(symbol: str):
    API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    try:
        quote = data["Global Quote"]

        return (
            f"{quote['01. symbol']} stock price is {quote['05. price']} "
            f"({quote['10. change percent']} change)"
        )

    except:
        return "Unable to fetch stock data"
available_tools = {
    "get_weather": get_weather, #using get_weather function where we designed our weather api calling logic
    "run_command": run_command, #using run_commad function where we designed our running system commands logic.
    "get_stock_price": get_stock_price 
}

SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Don't do all steps one at a time, go one by one, step by step response
    - If user mentions stock symbols like AAPL, TSLA, MSFT, INFY → ALWAYS use get_stock_price
    - If user asks price, stock, share, market → use get_stock_price
    - NEVER use get_weather for financial queries
    - NEVER confuse weather and stock tools

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "get_weather": Takes a city name as an input and returns the current weather for the city
    - "run_command": Takes linux command as a string and executes the command and returns the output after executing it.
    - "get_stock_price": Takes a stock symbol like AAPL, TSLA, INFY and returns current stock price using Alpha Vantage API.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
    Output: {{ "step": "plan", "content": "User is asking for stock market data" }}
    Output: {{ "step": "plan", "content": "I should use get_stock_price tool" }}
    Output: {{ "step": "action", "function": "get_stock_price", "input": "AAPL" }}
    Output: {{ "step": "observe", "output": "AAPL stock price is 189.23 (1.2% change)" }}
    Output: {{ "step": "output", "content": "AAPL is trading at $189.23." }}

"""

def run_agent(query):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query}
    ]

    logs = []

    while True:

        response = client.chat.completions.create(
            model="qwen2.5-coder:3b",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })

        parsed_response = json.loads(
            response.choices[0].message.content
        )

        if parsed_response.get("step") == "plan":

            logs.append(
                f"🧠 {parsed_response.get('content')}"
            )

            continue

        if parsed_response.get("step") == "action":

            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            if tool_name == "get_weather" and "stock" in query.lower():
                logs.append("❌ Blocked wrong tool selection")
                continue

            logs.append(
                f"🛠️ Calling Tool: {tool_name}({tool_input})"
            )

            if available_tools.get(tool_name):

                output = available_tools[tool_name](tool_input)

                logs.append(
                    f"👀 {output}"
                )

                messages.append({
                    "role": "user",
                    "content": json.dumps({
                        "step": "observe",
                        "output": output
                    })
                })

                continue

        if parsed_response.get("step") == "output":

            return {
                "answer": parsed_response.get("content"),
                "logs": logs
            }
