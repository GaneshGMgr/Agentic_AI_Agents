# SoftwareEngineers Crew

A CrewAI-powered autonomous agent system that transforms natural language software requirements into production-ready Python modules. Simulates a full software team with agents acting as engineering lead, backend developer, test engineer, and frontend UI creator. Uses local LLMs via Ollama (LLaMA3, Mistral, DeepSeek) to generate designs, code, unit tests, and Gradio-based demos — fully offline.

## 🛠 Installation & Setup

### Step 1: Install `uv` (fast Python package manager)

```bash
pip install uv
```

### Step 2: (Optional but recommended) Install dependencies with CrewAI

```bash
crewai install
```

### Step 3: Create a new crew from the predefined template

```bash
crewai create crew software_engineers
```

### Step 4: Activate the virtual environment

```bash
.\.venv\Scripts\activate  # Windows
# Or
source .venv/bin/activate  # macOS/Linux
```

### Step 5: Start the Ollama LLM server

```bash
ollama server
```

> This launches the Ollama server locally, which provides models like LLaMA, DeepSeek, Mistral, etc.

### Step 6: Run your CrewAI team

```bash
crewai run
```

> This kicks off your multi-agent software engineering crew using the configurations and task workflows defined.

---

## 💬 Support & Community

- 📄 [Documentation](https://docs.crewai.com)
- 💬 [GitHub Discussions](https://github.com/joaomdmoura/crewai)
- 🧵 [Discord Community](https://discord.com/invite/X4JWnZnxPb)
- 🤖 [Chat with Docs](https://chatg.pt/DWjSBZn)

---

Let's build powerful software modules with the simplicity of CrewAI and the autonomy of local LLMs! 🚀
