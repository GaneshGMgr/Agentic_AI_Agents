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

## 🖥️ Command to Run Server

```bash
ollama serve
uvicorn app:app --host 0.0.0.0 --port 8000

# or for hot-reload during development
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

---
