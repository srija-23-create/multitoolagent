# Multi Tool AI Agent

A modular AI agent built using Python, Ollama, and Streamlit that performs intelligent tool selection and executes tasks through a structured reasoning workflow. The agent follows a **Plan → Action → Observe → Output** framework to analyze user requests, invoke appropriate tools, and generate responses.

## Features

* Local LLM integration using Ollama
* Multi-tool architecture with dynamic tool invocation
* Structured reasoning and decision-making workflow
* Weather information retrieval
* Stock price retrieval
* System command execution
* Interactive web interface using Streamlit
* Extensible framework for adding new tools

---

## Architecture

```text
User Query
     |
     v
Large Language Model (Ollama)
     |
     v
Plan
     |
     v
Action
     |
     v
Tool Execution
     |
     v
Observation
     |
     v
Final Response
```

---

## Project Structure

```text
multi-tool-agent/
│
├── app.py                  # Streamlit application
├── agent.py                # Agent logic and tool implementations
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
└── README.md
```

---

## Technologies Used

* Python
* Streamlit
* Ollama
* OpenAI Python SDK
* Requests
* Python Dotenv

---

## Available Tools

### Weather Tool

Retrieves real-time weather information for a given city using the wttr.in API.

```python
get_weather(city)
```

---

### Stock Price Tool

Retrieves current stock prices and percentage changes using the Alpha Vantage API.

```python
get_stock_price(symbol)
```

Examples:

* AAPL
* TSLA
* MSFT
* INFY

---

### Command Execution Tool

Executes operating system commands and returns the execution result.

```python
run_command(command)
```

Examples:

```bash
dir
ls
pwd
```

---

## Agent Workflow

The agent operates using the following reasoning loop:

1. Analyze the user query.
2. Generate a plan for solving the request.
3. Select the appropriate tool.
4. Execute the selected tool.
5. Observe the tool output.
6. Produce the final response.

Example:

```text
User Query:
What is the weather in London?

Plan:
User requires weather information.

Action:
Invoke get_weather("London").

Observation:
The weather in London is Partly Cloudy +25°C.

Output:
Provide the weather information to the user.
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/multi-tool-agent.git
cd multi-tool-agent
```

### Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

```text
streamlit
openai
python-dotenv
requests
```

---

## Setup

### Install Ollama

Download and install Ollama from:

https://ollama.com

Pull the required model:

```bash
ollama pull qwen2.5-coder:3b
```

Start the Ollama server:

```bash
ollama serve
```

---

### Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=ollama
ALPHA_VANTAGE_API_KEY=YOUR_API_KEY
```

---

## Running the Application

```bash
streamlit run app.py
```

---

## Sample Queries

```text
What is the weather in Hyderabad?
```

```text
What is the stock price of AAPL?
```

```text
Run the command dir
```

---

## Extending the Agent

New tools can be added by:

1. Creating a tool function.
2. Registering it in `available_tools`.
3. Updating the system prompt with the tool description.

Example:

```python
def get_news(topic):
    pass

available_tools["get_news"] = get_news
```

---

## Future Enhancements

* Web search integration
* Memory and conversation history
* Additional utility tools
* Multi-agent collaboration
* Document processing capabilities
* Voice interaction support

---

## Author

**Srija Ayengar**
