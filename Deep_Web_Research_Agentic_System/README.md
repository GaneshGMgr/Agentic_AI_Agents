# 🧠✈️ Agentic AI-Based Autonomous Traders

---

## 📚 Resources

- [YouTube Video](https://www.youtube.com/watch?v=LSk5KaEGVk4&list=PLRDl2inPrWQXSDfCjPKSeEMFLwYpfytxH)
- [GitHub Repository](https://github.com/ed-donner/action/tree/main/1_deep_research)
- [Github agentic_search_openai_langgraph](https://github.com/menonpg/agentic_search_openai_langgraph/blob/main/tools.py)

---

### 🔧 Tools & APIs Used

1. **Redis Cache** (for fast access / context memory)  
   📄 Docs: [https://redis.io/docs/](https://redis.io/docs/)

2. **Coreference Resolution**  
   🔍 Model: `biu-nlp/f-coref` on HuggingFace

3. **Personal Assistants**  
   🧠 General concept; implement with AI frameworks or custom code

4. **Scholarly** (Google Scholar scraping library)  
   📦 PyPI: [https://pypi.org/project/scholarly/](https://pypi.org/project/scholarly/)

5. **arXiv API**  
   🔗 Endpoint: `http://export.arxiv.org/api/{method_name}?{parameters}`  
   📖 Docs: [https://info.arxiv.org/help/api/user-manual.html#Quickstart](https://info.arxiv.org/help/api/user-manual.html#Quickstart)

6. **Springer Nature Open Access API**  
   🌐 URL: [https://datasolutions.springernature.com/account/api-management/](https://datasolutions.springernature.com/account/api-management/)  
   📌 Usage Example:  
   `https://api.springernature.com/openaccess/jats?q=deep+learning&api_key=d6cb4879663fcda4dd`

7. **PubMed** (Biomedical papers)  
   🔗 URL: [https://account.ncbi.nlm.nih.gov/settings/](https://account.ncbi.nlm.nih.gov/settings/)

8. **ScienceDirect (Elsevier)**  
   🌍 URL: [https://dev.elsevier.com/apikey/manage](https://dev.elsevier.com/apikey/manage)  
   🏷️ Label: `ScienceDirectQueryTool`

9. **Semantic Scholar API**  
   🛠️ Endpoint: `https://api.semanticscholar.org/graph/v1/paper/batch`  
   📘 Docs: [https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_get_paper_autocomplete](https://api.semanticscholar.org/api-docs/#tag/Paper-Data/operation/get_graph_get_paper_autocomplete)

---


# command to run server
ollama serve
uvicorn app:app --host 0.0.0.0 --port 8000

uvicorn app:app --reload --host 0.0.0.0 --port 8000



🧠 research_paper — Mentions academic/research sources
These should all be classified as research_paper:

"Generate a report using academic studies on climate change."

"Summarize the latest findings from research papers on AI ethics."

"Prove your answer with scholarly articles."

"I want evidence from research papers on the effectiveness of remote learning."

"Provide insights from peer-reviewed studies about mental health."

"Explain using research papers how sleep affects productivity."

📄 report_generation — General requests without needing academic sources
These should be classified as report_generation:

"Write a report on the history of the internet."

"Summarize the impact of social media on teenagers."

"Generate a report about the benefits of exercise."

"Create a short report on global warming for school."

"Write a brief summary of renewable energy technologies."

Even though these sound formal, none ask for academic or research-backed material — so they should fall under report_generation.

🌐 google_search — Basic, factual, or current-event questions
These should be classified as google_search:

"Who is the current Prime Minister of Canada?"

"What is the population of Tokyo?"

"Best smartphones under $500 in 2025."

"When was the iPhone 16 released?"

"Where is the Eiffel Tower located?"

