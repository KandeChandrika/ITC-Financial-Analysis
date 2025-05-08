# 📊 ITC Sustainability Analyzer APP – AI-Powered Financial Q&A

An interactive AI app to explore ITC Ltd’s **sustainability efforts in 2024**, combining vector embeddings, Google Gemini, and LangChain inside a simple and clean **Streamlit** interface. This app provides factual, citation-backed answers with traceability to original report documents.

---

## 🌟 Key Capabilities

- 🤖 **Smart Embedding Loader**: Loads pre-processed financial documents from a local `Chroma` vector store.
- 🧬 **Embedding Engine**: Uses `GoogleGenerativeAIEmbeddings` for encoding financial text into vector format.
- 🧠 **Conversational AI**: Powered by `Gemini 2.0 Flash`, answering questions with precision and full citation.
- 🖥️ **Streamlit Interface**: A user-friendly frontend to interact with ITC’s sustainability insights.

---

## 🔧 Project Modules and Pipeline

---

### 📁 1. Data Scraping (Handled Separately)

> ⚠️ Not handled in the current app. The documents must be scraped manually or via a separate script using **Tavily**, **Firecrawl**, or **Crew AI**.

Example (Tavily):

```python
from tavily import Tavily

api_key = "your_tavily_api_key"
client = Tavily(api_key)

url = "https://www.itcportal.com/investor-relations/financial-reports/"
response = client.scrape_pdf(url)

extracted_text = response['text']
metadata = response['metadata']
print(extracted_text[:500])
print(metadata)

### 📁 2. Data Storage in Chroma Vector DB

The **scraped financial documents** (e.g., ITC’s reports) are **chunked**, **embedded**, and **stored locally** in a Chroma vector database, enabling efficient semantic search.

---

#### 📂 Required Files in `./chroma_db`

The following files must be present in the `chroma_db` directory:

- `chroma.sqlite3` – The main Chroma database file
- `index` files – Metadata and vector index files for fast retrieval
- `data_level0.bin` – Binary file containing document-level vector data
- Other auxiliary Chroma files (e.g., `lock`, `manifest.json`, etc.)

---

#### 🔒 Deployment Note

> These files must be **pre-generated** during embedding and should be **included with your deployment** (e.g., zipped as `chroma_db.zip`).

Once deployed, the app will load this Chroma vector store to enable question answering over the stored financial content.

### 🧠 3. Embedding Layer (`/embeddings`)

This module transforms raw financial text into dense vector representations for semantic search and retrieval.

---

#### 🔄 Text Chunking

- Performed using `RecursiveCharacterTextSplitter` from **LangChain**
- Breaks long documents into overlapping, manageable chunks for better context retention

---

#### ⚙️ Embedding Generation

- Uses **GoogleGenerativeAIEmbeddings** with the model `embedding-001`
- Requires a valid `GOOGLE_API_KEY` for authentication
- Produces dense vectors optimized for use with Google Gemini LLMs

---

#### 🗃️ Vector Storage

- Embedded chunks are stored in a **local Chroma vector database** located at:

---

#### 🧳 Deployment Optimization

- The `load_vector_store()` function in `streamlit_app.py` uses:
```python
@st.cache_resource

#### 🧠 3. Embedding Layer (`/embeddings`)

This module transforms raw financial text into dense vector representations for semantic search and retrieval.

#### 🔄 Text Chunking

- Performed using `RecursiveCharacterTextSplitter` from **LangChain**
- Breaks long documents into overlapping, manageable chunks for better context retention

#### ⚙️ Embedding Generation

- Uses **GoogleGenerativeAIEmbeddings** with the model `embedding-001`
- Requires a valid `GOOGLE_API_KEY` for authentication
- Produces dense vectors optimized for use with Google Gemini LLMs

#### 🗃️ Vector Storage

- Embedded chunks are stored in a **local Chroma vector database** located at:
  ```
  ./chroma_db
  ```

#### 🧳 Deployment Optimization

- The `load_vector_store()` function in `streamlit_app.py` uses:
  ```python
  @st.cache_resource
  ```


  ```
  to cache and reuse the vector store across sessions, reducing load time and boosting performance.

---

### 💬 4. LLM Query Interface (`/llm`)

- 🤖 LLM: `ChatGoogleGenerativeAI` using **Gemini 2.0 Flash**
- 🎯 Retriever: **MMR (Maximal Marginal Relevance)** for better diversity
- 📄 Cites source documents, showing metadata and preview snippets
- 🔒 API key pulled securely via `st.secrets["GOOGLE_API_KEY"]`

---

### 🖼️ 5. Streamlit Chat App (`streamlit_app.py`)

#### 🎯 Goal: Visual frontend for real-time Q&A

##### Key Features:
- 💬 Text input box for questions like:
  - “Summarize ITC's sustainability efforts in 2024.”
  - “List green initiatives by ITC in 2023–2024.”
- 🔎 AI-powered answer from Gemini
- 🧾 Source documents shown with:
  - Metadata (year, type, etc.)
  - Preview of raw content

##### Sidebar:
- 📘 About the app and tech stack
- 📋 Instructions for usage
- 🛠️ Troubleshooting tips

---

## ✅ Deployment Checklist

- [ ] Upload your `chroma_db` directory
- [ ] Add your `GOOGLE_API_KEY` to `.streamlit/secrets.toml`
- [ ] Run: `streamlit run streamlit_app.py`

---

## 🧠 Tech Stack

- **Streamlit** – For the web interface
- **LangChain** – For RAG and retrievers
- **Google Gemini 2.0 Flash** – As the language model
- **Chroma DB** – Local vector store
- **GoogleGenerativeAIEmbeddings** – For creating embeddings

---

> Built with ❤️ using Streamlit | Powered by Gemini & LangChain
