# NEA Waste Management RAG System

A complete Retrieval-Augmented Generation (RAG) system for NEA waste management data using Ollama, LangChain, and FAISS.

## 🚀 Features

- **Local LLM**: Uses Ollama with Llama-3-8B-Instruct (no license fees)
- **Smart Retrieval**: FAISS vector store for efficient document search
- **Knowledge Base**: 15+ markdown snippets from NEA waste statistics
- **Web Interface**: Beautiful Flask web app for easy interaction
- **Conversational Memory**: Maintains chat history for context
- **Source Attribution**: Shows which documents were used for answers

## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running
- Llama-3 model pulled
- 8GB+ RAM (for Llama-3-8B)

## 🛠️ Installation

### 1. Install Ollama

**Windows:**
```bash
# Download from https://ollama.ai/download
# Run the installer and restart terminal
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull Llama-3 Model

```bash
ollama pull llama3
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Knowledge Base

```bash
# First, scrape the data (if not already done)
python scripts/scrape.py

# Then generate the RAG knowledge base
python scripts/generate_rag_kb.py
```

## 🚀 Quick Start

### Option 1: Automated Setup

```bash
python scripts/setup_ollama.py
```

This script will:
- Check Ollama installation
- Verify Llama-3 model
- Install Python dependencies
- Test the RAG system

### Option 2: Manual Setup

1. **Start Ollama service:**
   ```bash
   ollama serve
   ```

2. **Run the RAG system:**
   ```bash
   python rag_system.py
   ```

3. **Or use the web interface:**
   ```bash
   python web_interface.py
   ```
   Then open http://localhost:5000

## 📚 Knowledge Base Content

The system includes 15+ knowledge snippets covering:

- **Key Statistics**: 2023 waste generation and recycling rates
- **Annual Data**: Year-by-year trends (2013-2023)
- **Material-Specific Rates**: Recycling rates by material type
- **Household Participation**: Survey results and trends
- **Policy Information**: NEA initiatives and programs

### Sample Questions You Can Ask:

- "What is the current recycling rate in Singapore?"
- "Can I recycle styrofoam?"
- "How much waste was generated in 2023?"
- "What is the household recycling participation rate?"
- "What are the recycling rates for different materials?"
- "How has waste generation changed over the past decade?"

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │  Command Line   │    │   Knowledge     │
│   (Flask App)   │    │   Interface     │    │     Base        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   RAG System    │
                    │   (LangChain)   │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FAISS Vector  │    │   Ollama LLM    │    │  HuggingFace    │
│     Store       │    │  (Llama-3-8B)   │    │  Embeddings     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Configuration

### Model Settings

Edit `rag_system.py` to adjust LLM parameters:

```python
llm = Ollama(
    model="llama3",
    temperature=0.1,      # Lower = more focused answers
    top_p=0.9,           # Nucleus sampling
    repeat_penalty=1.1    # Reduce repetition
)
```

### Retrieval Settings

Adjust the number of documents retrieved:

```python
retriever=self.vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Number of documents to retrieve
)
```

## 📊 Performance

- **Response Time**: 2-5 seconds per question
- **Memory Usage**: ~4GB for Llama-3-8B
- **Accuracy**: Grounded in NEA official data
- **Speed**: ~6 tokens/second on CPU

## 🐛 Troubleshooting

### Common Issues

1. **"Ollama is not running"**
   ```bash
   ollama serve
   ```

2. **"Model not found"**
   ```bash
   ollama pull llama3
   ```

3. **"Import errors"**
   ```bash
   pip install -r requirements.txt
   ```

4. **"Knowledge base not found"**
   ```bash
   python scripts/generate_rag_kb.py
   ```

### Performance Tips

- **Reduce model size**: Use `llama3:3b` for faster responses
- **Adjust chunk size**: Modify `chunk_size` in text splitter
- **Use GPU**: Install CUDA version of PyTorch for GPU acceleration

## 🔄 Updating Knowledge Base

To update with new data:

1. **Re-scrape data:**
   ```bash
   python scripts/scrape.py
   ```

2. **Regenerate knowledge base:**
   ```bash
   python scripts/generate_rag_kb.py
   ```

3. **Restart RAG system:**
   ```bash
   python rag_system.py
   ```

## 📁 File Structure

```
RecycleBot-Lite/
├── rag_system.py              # Main RAG system
├── web_interface.py           # Flask web app
├── setup_ollama.py            # Setup script
├── generate_rag_kb.py         # Knowledge base generator
├── scrape.py                  # Data scraper
├── requirements.txt           # Dependencies
├── data/
│   ├── raw/                   # Scraped JSON data
│   ├── knowledge_base/        # Markdown snippets
│   └── vector_store/          # FAISS index
├── templates/                 # Web interface templates
└── docs/                      # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **NEA**: For providing comprehensive waste management data
- **Ollama**: For the excellent local LLM framework
- **LangChain**: For the RAG framework
- **FAISS**: For efficient vector search
- **HuggingFace**: For embeddings and models

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review the logs for error messages
3. Ensure all dependencies are installed
4. Verify Ollama is running correctly

---

**Happy RAG-ing! 🗑️♻️** 