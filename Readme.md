# **Observability RAG Assistant**  
**AI-powered server monitoring with natural language queries**  

---

## **🚀 Features**  
✅ **Natural Language Processing** - Ask questions like "Show servers with high CPU"  
✅ **Dual Interfaces** - CLI for experts & Web UI for visualization  
✅ **Local Execution** - Runs entirely on your machine (DuckDB + Ollama)  
✅ **Dark/Light Mode** - Eye-friendly interface with smooth animations  
✅ **Optimized Performance** - Indexed database + quantized LLMs  

---

## **⚡ Quick Start**  

### **1. Install Requirements**  
```bash
# Core dependencies
pip install -r requirements.txt

# Download optimized LLM (1.6GB)
ollama pull  llama3.2:1b
```

### **2. Initialize System**  
```bash
# Generate sample telemetry (10 servers, 7 days data)
python data_generator.py

# Setup optimized database
python db_setup.py
```

### **3. Launch Interface**  


 
####  CLI**  
```bash
python cli.py
```

---

## **🔍 Sample Queries**  

```sql
"Show top 3 servers by memory usage today"  
"Find hosts with disk >90% in last 6 hours"  
"Compare CPU spikes between 2-4 PM yesterday"  
"Which services had abnormal metrics this week?"
```

---

## **🛠️ Architecture**  

```mermaid
flowchart LR
    A[User Query] --> B[LLM SQL Generator]
    B --> C[DuckDB Engine]
    C --> D[Result Analyzer]
    D --> E{{Formatted Response}}
```

**Key Components:**  
- **RAG Core**: `rag_core.py` (Query processing brain)  
- **Web Interface**: `web_ui.py` (Gradio-powered)  
- **CLI**: `cli.py` (For terminal lovers)  
- **Database**: DuckDB with automatic indexing  

---

**Pro Tip:** For GPU acceleration:  
```python
# In rag_core.py
ChatOllama(model="mistral", num_gpu=1)
```
---

### File Structure
observability-rag
/

├── docs/

│ ├── CLI_demo.mp4

│ ├── UI_demo.mp4

│ ├── cli_thumbnail.png

│ └── ui_thumbnail.png

├── data_generator.py

├── db_setup.py

├── rag_core.py

├── cli.py

├── requirements.txt

└── README.md


---

## **🚨 Troubleshooting**  

| Symptom | Solution |
|---------|----------|
| Port 7860 busy | Use `python web_ui.py --port 7861` |
| Slow responses | Try `ollama pull mistral:7b-instruct-q4_K_M` |
| SQL errors | Check `python db_setup.py --reset` |

---

💡 **Pro Tip:** Bookmark [localhost:7860](http://localhost:7860) 

---

**▶️ Watch Full Demos:**  
- [CLI Walkthrough](docs/CLI_demo.mp4)  
- [Web UI Tutorial](docs/UI_demo.mp4)  

```
