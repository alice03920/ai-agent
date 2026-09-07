# 🤖 AI Coding Agent

Hi! I’m Alice 😊
I built this project to learn how modern AI coding agents actually work under the hood.

Rather than just sending prompts to an LLM, this agent can **inspect files, read code, modify files, run Python programs, and use the results of those actions to decide what to do next**.

---

## ✨ What It Does

My agent can:

- 📂 List files and directories
- 📖 Read source code
- ✏️ Create and overwrite files
- ▶️ Run Python programs and tests
- 🔁 Feed tool results back into the LLM
- 🐛 Investigate and fix simple bugs autonomously

The basic loop looks like:

```text
User request
   ↓
LLM chooses a tool
   ↓
Python executes it
   ↓
Result goes back to the LLM
   ↓
Agent decides what to do next
   ↓
Final response
```

---

## 🧠 How I Built It

I created four tools for the agent:

- `get_files_info`
- `get_file_content`
- `write_file`
- `run_python_file`

I then described those tools to the LLM using **JSON function schemas**.

When the model requests a tool, my Python code maps the requested function name to the real function and executes it.

```python
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}
```

I also built an **agent loop**, allowing the model to use multiple tools in sequence instead of stopping after one action.

---

## 🐛 My Favourite Part

The final challenge was really satisfying!

I deliberately broke the calculator's operator precedence so:

```text
3 + 7 * 2
```

incorrectly returned:

```text
20
```

I then asked my agent to fix the bug.

It inspected the project, found the relevant source file, identified the incorrect precedence value, **edited the code itself**, and restored the correct behaviour.

Watching it change the broken code back automatically was definitely the moment the whole project clicked for me. 😭

---

## 💥 Things I Struggled With

This project was definitely not smooth sailing!

A few things confused me along the way:

- understanding how LLM tool calls actually work
- getting the function schemas correct
- handling JSON arguments
- debugging imports between different modules
- keeping the two different `main.py` files straight 😭
- getting the model to choose the correct tool consistently
- understanding how the agent loop keeps conversation history in sync

I made quite a few mistakes while putting everything together, but debugging those mistakes helped me understand the architecture much better.

Instead of just thinking:

> “the AI somehow runs a function”

I now understand the actual process:

```text
LLM requests function
→ Python validates request
→ Python executes function
→ result becomes a tool message
→ result goes back to LLM
```

That was probably my biggest takeaway from the project.

---

## 🔐 Security

Because this agent can execute Python and modify files, I restricted it to the:

```text
./calculator
```

directory.

The agent does **not** get to choose its own working directory, and filesystem functions reject paths that escape the permitted directory.

I also store my OpenRouter API key in a local `.env` file which is excluded from GitHub using `.gitignore`.

> ⚠️ This is still an educational project, not a production-grade sandbox.

---

## 🛠️ Tech I Used

- 🐍 Python
- 🤖 LLM APIs
- 🌐 OpenRouter
- 🔌 Tool / function calling
- 🧾 JSON Schema
- 🔄 Agent loops
- 📂 Filesystem operations
- ▶️ `subprocess`
- 🧪 Automated tests
- 🔐 Environment variables
- 🌳 Git & GitHub
- 📦 uv

---

## 📁 Project Structure

```text
ai-agent/
├── calculator/
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── call_function.py
├── main.py
├── prompts.py
└── tests...
```

---

## 🚀 Running It

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_api_key_here
```

Then run:

```bash
uv run main.py "Explain how the calculator works"
```

Or see the agent's tool usage:

```bash
uv run main.py "Fix the bug in the calculator" --verbose
```

---

## 🌱 What I Learned

This project gave me my first proper look at how an AI agent can move beyond simply generating text.

I learned how to connect an LLM to real code, let it interact with a codebase, give it feedback from its own actions, and build safeguards around what it is allowed to do.

It was challenging in places, but getting the final autonomous bug-fixing flow working made it very worth it. 💜

---

## 👩🏽‍💻 About Me

I’m **Alice**, a software engineering self-learning student interested in full-stack development.

I really enjoy full stack in general, but this project was specifically because I was really interested in understanding the fundamentals of how LLMs work!
