\# 🤖 Autonomous Multi-Agent AI System



\## 🌐 Live Demo



\*\*Deployed on Railway:\*\* \[https://autonomous-ai-agent-production.up.railway.app](https://autonomous-ai-agent-production.up.railway.app)



> The system is live and running autonomously on the cloud!



\[!\[Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/autonomous-ai-agent)



> Ever wondered what happens when you give AI agents their own team? This is my attempt at building that - a system where specialized AI agents work together to solve complex tasks autonomously.



\[!\[Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

\[!\[Groq](https://img.shields.io/badge/LLM-Groq-green.svg)](https://groq.com/)



\## 🎯 What Is This?



Think of this as a small AI company in a box. You give it a task, and a team of specialized AI agents figures out how to get it done - no human hand-holding required.



I built this to explore multi-agent systems and showcase what modern AI can do when you combine autonomous reasoning with good software architecture. It's been a fun journey from "I wonder if this is possible" to "holy cow, it actually works!"



\## 💡 The Story Behind It



As a Data Scientist, I've worked with plenty of AI models, but they usually work in isolation. I got curious: \*\*What if AI agents could collaborate like a real team?\*\*



So I built:

\- A \*\*Research Agent\*\* that hunts down academic papers (because who has time to read all of arXiv?)

\- A \*\*Data Agent\*\* that watches APIs like a hawk and yells when something breaks

\- An \*\*Intelligence Agent\*\* that stalks competitor websites (ethically, of course!)

\- An \*\*Orchestrator\*\* that manages this whole circus



The result? A system that can autonomously research transformers, monitor your APIs, and analyze websites - all while you grab coffee ☕



\## ✨ What Can It Actually Do?



\### 🔬 Research Agent - Your Academic Assistant

\*\*"Find me papers on transformers"\*\* → It searches arXiv, reads abstracts, and summarizes findings.



Real talk: I got tired of manually searching for papers. This agent does it in seconds and actually understands what it's looking at (thanks, LLMs!).



\### 📊 Data Agent - Your API Watchdog  

\*\*"Monitor this API"\*\* → It checks health, tracks response times, and detects anomalies.



The cool part? It learns what "normal" looks like and alerts you when things get weird. Like when your API suddenly takes 3x longer to respond - that's not just slow, that's a red flag 🚩



\### 🌐 Intelligence Agent - Your Web Detective

\*\*"Analyze this competitor's site"\*\* → It scrapes, extracts key info, and tracks changes over time.



I built this because I was manually checking competitor sites weekly. Now? The agent does it daily and tells me what changed.



\### 🎭 Orchestrator - The Team Manager

\*\*"Do all three things"\*\* → It figures out which agents to use and coordinates the whole operation.



This is the brain. You give it messy human instructions, and it translates that into a coordinated multi-agent plan. Pretty neat!



\## 🏗️ How It Works (The Simple Version)

You: "Monitor my API and find papers about it"

↓

Orchestrator: "Hmm, this needs Data Agent AND Research Agent"

↓

┌─────────────────┐

│  Orchestrator   │  ← Thinks about the task

└────────┬────────┘

│

┌────┴────┐

│         │

┌───▼──┐  ┌──▼────┐

│ Data │  │Research│ ← Work simultaneously

│Agent │  │ Agent  │

└───┬──┘  └──┬────┘

│        │

└────┬───┘

▼

Combined Results  ← You get the full picture



\## 🚀 Quick Start



\### You'll Need:

\- Python 3.8+ (you probably have this)

\- A free Groq API key (takes 2 minutes to get)

\- 5 minutes of your time



\### Get It Running:



```bash

\# 1. Grab the code

git clone https://github.com/keshavloma1081-ctrl/autonomous-ai-agent.git

cd autonomous-ai-agent



\# 2. Install dependencies (takes \~30 seconds)

pip install -r requirements.txt



\# 3. Add your free Groq API key

\# Get one from: https://console.groq.com/



\# For Windows:

echo GROQ\_API\_KEY=your\_key\_here > .env



\# For Mac/Linux:

echo "GROQ\_API\_KEY=your\_key\_here" > .env



\# 4. Fire it up!

python main.py

```



\### Your First Commands:



```bash

🤖 > help

\# See what you can do



🤖 > monitor https://httpbin.org/status/200

\# Watch it check API health in real-time



🤖 > analyze https://news.ycombinator.com  

\# See it scrape and analyze Hacker News



🤖 > research transformers

\# Find recent ML papers automatically

```



\*\*Pro tip:\*\* Start with `monitor` - it works instantly and shows you the whole system in action!



\## 🌐 REST API



The system includes a REST API for programmatic access!



\### Start the API Server



```bash

python api.py

```



The server will start on `http://localhost:5000`



\### Endpoints



\*\*GET /health\*\* - Check API health

```bash

curl http://localhost:5000/health

```



Response:

```json

{

&#x20; "status": "healthy",

&#x20; "timestamp": "2026-04-22T00:38:56",

&#x20; "agents\_available": 3

}

```



\*\*GET /agents\*\* - List available agents

```bash

curl http://localhost:5000/agents

```



\*\*POST /execute\*\* - Execute a task

```bash

curl -X POST http://localhost:5000/execute \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"task": "monitor https://httpbin.org/status/200"}'

```



\### Example Integration



```python

import requests



\# Execute a task via API

response = requests.post(

&#x20;   "http://localhost:5000/execute",

&#x20;   json={"task": "research transformers in NLP"}

)



result = response.json()

print(result)

```



\### Live API Deployment



\*\*API is deployed on Railway:\*\* https://autonomous-ai-agent-production.up.railway.app



Test the live API:

```bash

curl https://autonomous-ai-agent-production.up.railway.app/health

```



\## 📂 What's Inside?



I organized this like a real software project:

autonomous-ai-agent/

├── main.py              # Your command center

├── api.py               # REST API server

├── agents/              # Where the magic happens

│   ├── base\_agent.py       # Blueprint for all agents

│   ├── research\_agent.py   # The academic one

│   ├── data\_agent.py       # The monitor

│   ├── intelligence\_agent.py  # The detective

│   └── orchestrator\_agent.py  # The manager

├── core/                # The engine

│   └── llm\_client.py       # Talks to AI (Groq/Claude)

└── config/              # Settings

└── settings.py         # One place for all config



\## 🎓 What I Learned Building This



\### The Fun Stuff:

\- \*\*Multi-agent coordination is HARD\*\* - Getting agents to work together without stepping on each other's toes took way more debugging than expected

\- \*\*LLMs can actually reason\*\* - Watching agents "think" about tasks before executing them never gets old

\- \*\*Good architecture matters\*\* - The abstract base class saved me from rewriting the same code 4 times

\- \*\*Free doesn't mean bad\*\* - Groq's free tier is genuinely fast and capable



\### The Technical Wins:

\- Mastered abstract base classes (ABC pattern is 🔥)

\- Got really good at API error handling (because everything fails eventually)

\- Learned that anomaly detection is just fancy statistics

\- Discovered BeautifulSoup is underrated for web scraping

\- Realized Docker makes everything easier



\## 💭 Design Decisions (Why I Built It This Way)



\*\*Q: Why multiple agents instead of one big agent?\*\*  

A: Specialization. Would you ask your accountant to fix your car? Same logic here.



\*\*Q: Why Groq over OpenAI?\*\*  

A: It's FREE and fast. OpenAI is great, but this needed to be accessible to everyone.



\*\*Q: Why CLI instead of web UI?\*\*  

A: Wanted to nail the core logic first. UI is next on the roadmap!



\*\*Q: Why Python?\*\*  

A: Because life's too short for boilerplate. Plus, the AI/ML ecosystem is all Python anyway.



\## 📊 Real Performance Numbers



I tested this for a week. Here's what I found:



| What It Does | How Fast | Cost |

|-------------|---------|------|

| Monitor an API (3 checks) | \~6 seconds | $0.00 |

| Scrape a website | < 2 seconds | $0.00 |

| Find 5 research papers | \~3 seconds | $0.00 |

| Think about a task (LLM call) | \~1 second | $0.00 |

| \*\*Everything\*\* | \*\*Completely FREE\*\* | \*\*$0.00\*\* |



Yeah, it's all free. That was the goal.



\## 🚧 What's Next?



I've got some ideas brewing:



\- \[ ] \*\*Web Dashboard\*\* - Because sometimes you want to click buttons instead of typing

\- \[ ] \*\*Slack Integration\*\* - Get agent updates in Slack

\- \[ ] \*\*More Agents\*\* - Maybe a "Code Agent" that reviews PRs?

\- \[ ] \*\*Better Memory\*\* - Currently agents remember \~50 things. Let's make it smarter.

\- \[ ] \*\*Agent Communication\*\* - Let agents talk to each other directly

\- \[ ] \*\*Learning from Mistakes\*\* - Track what works and what doesn't



Want to contribute? PRs are welcome! Or just star it if you think it's cool ⭐



\## 🤔 FAQ



\*\*Q: Do I need to pay for anything?\*\*  

A: Nope! Groq's free tier handles everything.



\*\*Q: Can I use this for production?\*\*  

A: It's production-ready architecture, but add monitoring and error tracking first.



\*\*Q: Is this better than AutoGPT/BabyAGI?\*\*  

A: Different goals. This is more focused on specific tasks with specialized agents.



\*\*Q: Can I add my own agents?\*\*  

A: Absolutely! Inherit from `BaseAgent` and you're 80% done.



\*\*Q: How do you handle rate limits?\*\*  

A: Exponential backoff with retries. Works surprisingly well.



\## 👨‍💻 About Me



Hey! I'm \*\*Keshav Kumar\*\*, a Data Scientist and ML Engineer based in Delhi NCR. I've spent 4+ years building ML systems and got curious about multi-agent architectures.



This project started as "I wonder if I can..." and turned into something I'm genuinely proud of. If you're in ML/AI and want to chat about agents, LLMs, or just trade war stories about production ML, hit me up!



\- \*\*GitHub:\*\* \[@keshavloma1081-ctrl](https://github.com/keshavloma1081-ctrl)

\- \*\*LinkedIn:\*\* \[Connect with me](https://linkedin.com/in/your-profile)



\## 🙏 Thanks



Built this while learning about multi-agent systems. Special thanks to:

\- The Anthropic team for Claude (even though I'm using Groq now 😅)

\- Groq for actually free and fast LLM access

\- The Python community for BeautifulSoup, Requests, and everything else

\- Coffee ☕ (lots of it)



\## 📄 License



MIT License - basically, do whatever you want with this. Just don't blame me if your agents become sentient 🤖



\---



\*\*Found this interesting? Star it! ⭐\*\*  

\*\*Want to improve it? Open a PR!\*\*  

\*\*Just think it's cool? Tell your friends!\*\*



Built with curiosity, caffeine, and a lot of debugging.

