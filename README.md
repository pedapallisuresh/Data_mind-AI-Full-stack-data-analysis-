# Data_mind-AI-Full-stack-data-analysis-

A modern, full-stack data analysis application with AI-powered insights, natural language SQL query generation, and interactive visualizations. Built with React + Vite for the frontend and Flask for the backend.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)
- [Data Sources](#data-sources)
- [Development](#development)

---

## 🚀 Features

### Data Management
- **📤 Multiple Data Sources**: Upload CSV files, load from URLs, connect to REST APIs, query SQL databases, and integrate with data pipelines
- **📁 Multi-Dataset Support**: Manage multiple datasets simultaneously with easy switching between them
- **🔄 Data Cleaning**: Automatic removal of duplicates, handling missing values, and outlier detection

### Data Analysis
- **📊 Comprehensive Analysis**: Generate summaries, descriptive statistics, correlation matrices, and categorical insights
- **🔍 Data Profiling**: Detailed profiling including memory usage, data types, missing values, and unique value counts
- **📈 Statistical Tests**: Normality tests, skewness/kurtosis analysis, and high correlation detection

### AI-Powered Features
- **🤖 AI Insights**: Generate intelligent, business-focused insights using Large Language Models (LLM)
- **💬 Agent Chat**: Conversational AI agent for interactive data analysis
- **🧠 Natural Language Queries**: Ask questions in plain English and get SQL queries generated automatically

### Visualization
- **📊 Interactive Charts**: Histograms, bar charts, correlation heatmaps, and box plots
- **💡 Visualization Suggestions**: AI-powered recommendations for the best chart types for your data

---

## 🛠 Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Recharts** - Data visualization library
- **Axios** - HTTP client
- **Lucide React** - Icon library

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Pandas** - Data manipulation and analysis
- **DuckDB** - In-memory SQL database for query execution

### AI/ML
- **OpenAI API** - LLM for AI insights and query generation
- **Tavily API** - Alternative LLM provider (fallback)
- **Ollama** - Local LLM support

---

## 📂 Project Structure

```
ai_data_project/
├── api.py                    # Flask backend API
├── analyzer.py               # Data analysis modules
├── cleaner.py                # Data cleaning functions
├── qa_engine.py              # Natural language to SQL
├── requirements.txt          # Python dependencies
├── README.md                  # Project documentation
├── RUN.md                     # Running instructions
├── TODO.md                    # Development tasks
├── test_data.csv             # Sample test data
│
├── frontend/                  # React frontend
│   ├── package.json          # Node.js dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── index.html            # HTML entry point
│   └── src/
│       ├── main.jsx          # React entry point
│       ├── App.jsx           # Main application component
│       └── App.css           # Styles
│
└── venv/                      # Python virtual environment
```

---

## 🏁 Getting Started

### Prerequisites

| Software | Version |
|----------|---------|
| Node.js | 18+ |
| Python | 3.8+ |

### Installation Steps

#### 1. Clone and Navigate
```bash
cd c:\Users\pedapalli.s.lv\ai_data_project
```

#### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Alternative AI provider (optional)
TAVILY_API_KEY=your_tavily_api_key_here
```

#### 5. Start the Backend Server
```bash
python api.py
```
The API will run on `http://localhost:5000`

#### 6. Start the Frontend Development Server
```bash
cd frontend
npm run dev
```
The frontend will run on `http://localhost:3000`

#### 7. Open in Browser
Navigate to `http://localhost:3000` to use the application.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes* | OpenAI API key for AI features |
| `TAVILY_API_KEY` | No | Fallback AI provider |
| `PORT` | No | Backend port (default: 5000) |

*At least one AI provider key is required for AI features to work.

### Supported AI Providers

1. **OpenAI** (Primary) - GPT-3.5/GPT-4 models
2. **Ollama** (Local) - Run LLMs locally
3. **Tavily** (Fallback) - Alternative LLM provider

---

## 📡 API Endpoints

### Data Upload
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload CSV file |
| POST | `/upload/url` | Load data from URL |
| POST | `/upload/api` | Fetch data from REST API |
| POST | `/upload/database` | Query SQL database |
| POST | `/upload/pipeline` | Connect to data pipeline |

### Dataset Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/datasets` | List all datasets |
| POST | `/datasets/switch` | Switch active dataset |
| POST | `/datasets/delete` | Delete a dataset |

### Data Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/preview` | Get data preview |
| POST | `/clean` | Clean the data |
| GET | `/summary` | Get data summary |
| GET | `/source-info` | Get data source information |

### Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/comprehensive-analysis` | Full data analysis |
| GET | `/data-profiling` | Data profiling info |
| GET | `/statistical-summary` | Statistical tests |
| GET | `/comprehensive-agent-analysis` | Complete agent analysis |

### AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ai-insights` | AI-powered insights |
| GET | `/visualization-suggestions` | Chart suggestions |
| POST | `/query` | Execute natural language query |
| POST | `/agent-chat` | Conversational AI agent |

### Visualization
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/visualization-data` | Get chart data |

---

## 📖 Usage Guide

### 1. Uploading Data

#### From File
- Click **Upload** tab
- Select **File** source type
- Choose a CSV file from your computer

#### From URL
- Click **Upload** tab
- Select **URL** source type
- Enter the URL (CSV, JSON, or Excel)
- Click **Load Data**

#### From API
- Click **Upload** tab
- Select **API** source type
- Enter the API endpoint URL
- Optionally add headers (JSON format)
- Click **Fetch Data**

#### From Database
- Click **Upload** tab
- Select **Database** source type
- Choose database type (SQLite, PostgreSQL, MySQL)
- Enter connection string and SQL query
- Click **Execute Query**

#### From Pipeline
- Click **Upload** tab
- Select **Pipeline** source type
- Choose pipeline type (Airtable, Google Sheets, Snowflake, BigQuery, Databricks)
- Enter configuration details
- Click **Connect**

### 2. Data Cleaning

Navigate to the **Data Cleaning** tab and click **Clean Data** to:
- Remove duplicate rows
- Handle missing values (median for numeric, "Unknown" for categorical)
- Remove outliers using IQR method
- Standardize column names

### 3. Data Analysis

Navigate to the **Analysis** tab and click on any analysis card:
- **Summary**: Basic data overview
- **Comprehensive**: Full analysis with statistics
- **Profiling**: Data quality assessment
- **Visualizations**: Chart recommendations
- **Statistics**: Statistical tests
- **Agent Analysis**: Complete AI-powered analysis

### 4. AI Insights

Navigate to the **AI Insights** tab and click **Generate AI Insights** to receive:
- Key patterns and relationships
- Business recommendations
- Data quality assessment
- Analytical approaches
- Actionable insights

### 5. Natural Language Queries

Navigate to the **Query** tab and:
- Ask questions in plain English (e.g., "What is the average sales by region?")
- View the generated SQL query
- See the query results in a table

### 6. Agent Chat

Navigate to the **Agent Chat** tab to:
- Have a conversation with the AI about your data
- Ask follow-up questions
- Get contextual insights

### 7. Visualizations

Navigate to the **Visualizations** tab to:
- View histograms for numeric columns
- See bar charts for categorical data
- Check correlation heatmaps
- Analyze box plots for distribution

---

## 🔗 Data Sources

### Supported Sources

| Source | Formats | Description |
|--------|---------|-------------|
| File Upload | CSV | Local file upload |
| URL | CSV, JSON, Excel, Parquet | Load from web URL |
| REST API | JSON | Any REST API endpoint |
| SQLite | SQL | Local SQLite database |
| PostgreSQL | SQL | PostgreSQL database |
| MySQL | SQL | MySQL database |
| Airtable | - | Airtable base |
| Google Sheets | - | Google Sheets |
| Snowflake | SQL | Snowflake data warehouse |
| BigQuery | SQL | Google BigQuery |
| Databricks | SQL | Databricks |

---

## 🧑‍💻 Development

### Running in Development Mode

```bash
# Terminal 1 - Backend
python api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Building for Production

```bash
cd frontend
npm run build
```

### Adding New Features

1. **Backend**: Add new endpoints in `api.py`
2. **Analysis**: Add functions in `analyzer.py`
3. **Frontend**: Add components in `frontend/src/App.jsx`

---

## 🚀 Performance Optimization Techniques

### Backend Optimizations

#### 1. Caching Strategy
```python
# Implement Redis caching for expensive operations
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'RedisCache'})

@app.route('/comprehensive-analysis')
@cache.cached(timeout=300, query_string=True)
def comprehensive_analysis():
    # Expensive operation here
    pass
```

#### 2. Lazy Loading & Chunking
```python
# Process large files in chunks
def process_large_file(file_path, chunk_size=10000):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk

# Use streaming responses for large datasets
from flask import Response
import json

@app.route('/preview')
def preview():
    def generate():
        for chunk in process_large_file(current_file):
            yield json.dumps(chunk)
    return Response(generate(), mimetype='application/json')
```

#### 3. Database Query Optimization
```python
# Use DuckDB efficiently
con = duckdb.connect(database=':memory:')
con.execute("PRAGMA threads=4")  # Parallel processing
con.execute("PRAGMA memory_limit=2GB")  # Memory management
```

#### 4. Async Processing
```python
# Use Celery for background tasks
from celery import Celery

celery = Celery('app', broker='redis://localhost:6379')

@celery.task
def generate_ai_insights_async(df_id):
    # Run heavy AI operations in background
    pass
```

#### 5. Data Structure Optimization
```python
# Use efficient data types
df = pd.read_csv(file, dtype={
    'int_column': 'int32',  # Use int32 instead of int64
    'float_column': 'float32',  # Use float32 instead of float64
    'category_column': 'category'  # Use categorical dtype
})

# Memory optimization
df['text_column'] = df['text_column'].astype('category')
```

### Frontend Optimizations

#### 1. Memoization
```javascript
import { useMemo, useCallback } from 'react'

// Memoize expensive computations
const processedData = useMemo(() => {
  return largeDataset.map(item => transform(item))
}, [largeDataset])

// Memoize callback functions
const handleQuery = useCallback((query) => {
  // Query logic
}, [dependencies])
```

#### 2. Virtual Scrolling
```javascript
import { FixedSizeList } from 'react-window'

// For large data tables
<FixedSizeList
  height={500}
  itemCount={data.length}
  itemSize={35}
>
  {Row}
</FixedSizeList>
```

#### 3. Pagination & Lazy Loading
```javascript
// Load data in pages
const [page, setPage] = useState(1)
const pageSize = 100

const currentData = useMemo(() => {
  const start = (page - 1) * pageSize
  return fullData.slice(start, start + pageSize)
}, [page])
```

#### 4. API Request Debouncing
```javascript
import { useDebouncedCallback } from 'use-debounce'

const debouncedSearch = useDebouncedCallback((query) => {
  fetchResults(query)
}, 300)
```

### LLM Query Optimization

#### 1. Context Optimization
```python
def optimize_prompt(df, question):
    # Only include relevant columns
    relevant_cols = [col for col in df.columns if any(
        keyword in col.lower() for keyword in question.lower().split()
    )]
    
    # Limit data samples
    sample_df = df[relevant_cols].head(10)
    
    # Build minimal context
    context = f"Columns: {relevant_cols}\nData:\n{sample_df.to_string()}"
    return context
```

#### 2. Response Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_llm_query(prompt_hash, question):
    # Cache common queries
    return query_llm(prompt, question)
```

#### 3. Batch Processing
```python
# Process multiple insights in one call
def batch_generate_insights(df, insights_types):
    prompt = f"""
    Generate insights for each category:
    {insights_types}
    
    Data: {df.head(20).to_string()}
    """
    return query_llm(prompt)
```

---

## 🤖 Alternative LLM Integration Methods

### 1. Hugging Face Transformers (Local)

```python
# Install: pip install transformers torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Initialize local model
model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, 
    torch_dtype=torch.float16,
    device_map="auto"
)

def query_local_model(prompt, system_prompt="You are a data analysis assistant."):
    full_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
    
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        temperature=0.7,
        do_sample=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 2. LangChain Integration

```python
# Install: pip install langchain langchain-openai langchain-community
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import create_csv_agent

# OpenAI LangChain
llm = ChatOpenAI(model="gpt-4", temperature=0)

# CSV Agent for data analysis
agent = create_csv_agent(llm, "data.csv", verbose=True)

# Run analysis
result = agent.run("What is the average sales by region?")

# Custom chain for insights
prompt = PromptTemplate(
    input_variables=["data_summary", "question"],
    template="Analyze this data: {data_summary}\n\nQuestion: {question}"
)

chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run({"data_summary": summary, "question": question})
```

### 3. LlamaIndex (RAG-based)

```python
# Install: pip install llamaindex
from llama_index import GPTListIndex, LLMPredictor
from llama_index import ServiceContext
from langchain import OpenAI

# Build index from DataFrame
from llama_index import GPTSimpleVectorIndex
import pandas as pd

df = pd.read_csv("data.csv")
documents = [Document(text=str(row)) for _, row in df.iterrows()]

index = GPTSimpleVectorIndex(documents)

# Query
response = index.query("What are the key insights from this data?")
```

### 4. Anthropic Claude API

```python
# Install: pip install anthropic
import anthropic

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def query_claude(prompt, system_prompt="You are a data analysis assistant."):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
```

### 5. Azure OpenAI

```python
# Install: pip install openai
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def query_azure(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a data analysis assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
```

### 6. Google Gemini API

```python
# Install: pip install google-generativeai
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def query_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
```

### 7. Local LLM with llama.cpp

```python
# Install: pip install llama-cpp-python
from llama_cpp import Llama

# Load quantized model
llm = Llama(
    model_path="models/llama-7b-chat.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)

def query_local_llama(prompt):
    output = llm(
        f"System: You are a data analysis assistant.\n\nUser: {prompt}\n\nAssistant:",
        max_tokens=500,
        temperature=0.7
    )
    return output['choices'][0]['text']
```

### 8. vLLM (Production Local)

```python
# Install: pip install vllm
from vllm import LLM, SamplingParams

# Initialize vLLM server
llm = LLM(model="meta-llama/Llama-2-7b-chat-hf")

def query_vllm(prompt):
    sampling_params = SamplingParams(
        temperature=0.7,
        max_tokens=500
    )
    outputs = llm.generate([prompt], sampling_params)
    return outputs[0].outputs[0].text
```

### 9. AWS Bedrock

```python
# Install: pip install boto3
import boto3
import json

bedrock = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
)

def query_bedrock(prompt):
    body = json.dumps({
        "prompt": f"Human: {prompt}\nAssistant:",
        "max_tokens_to_sample": 1000,
        "temperature": 0.7
    })
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        contentType='application/json',
        accept='application/json',
        body=body
    )
    
    return json.loads(response['body'].read())['completion']
```

### 10. Custom LLM Wrapper

```python
# Generic LLM wrapper for any API
class LLMWrapper:
    def __init__(self, provider, api_key, **kwargs):
        self.provider = provider
        self.config = {'api_key': api_key, **kwargs}
    
    def query(self, prompt, system_prompt=None):
        if self.provider == 'openai':
            return self._query_openai(prompt, system_prompt)
        elif self.provider == 'anthropic':
            return self._query_anthropic(prompt, system_prompt)
        elif self.provider == 'local':
            return self._query_local(prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    def _query_openai(self, prompt, system_prompt):
        # OpenAI implementation
        pass
    
    def _query_anthropic(self, prompt, system_prompt):
        # Anthropic implementation
        pass
    
    def _query_local(self, prompt):
        # Local model implementation
        pass

# Usage
llm = LLMWrapper(
    provider='openai',
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-4'
)
result = llm.query("Analyze this data...")
```

### 11. LiteLLM (Unified Interface)

```python
# Install: pip install litellm
import litellm

# Works with 100+ LLM models with unified API
response = litellm.completion(
    model="gpt-4",
    messages=[{"content": "Analyze this data", "role": "user"}]
)

# Switch models easily
response = litellm.completion(
    model="claude-3-opus-20240229",
    messages=[{"content": "Analyze this data", "role": "user"}]
)

# Use local models
response = litellm.completion(
    model="ollama/llama2",
    messages=[{"content": "Analyze this data", "role": "user"}]
)
```

### 12. HuggingFace Inference Endpoints

```python
# Install: pip install huggingface_hub
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="meta-llama/Llama-2-70b-chat-hf",
    token=os.getenv("HF_TOKEN")
)

def query_hf_inference(prompt):
    response = client.text_generation(
        prompt,
        max_new_tokens=500,
        temperature=0.7
    )
    return response
```

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

For issues or questions, please check:
1. `RUN.md` - Detailed running instructions
2. `TODO.md` - Development roadmap
3. Environment variables are properly configured

---

## Future Enhancements

- 🔮 [ ] Additional visualization types
- [ ] More data pipeline integrations
- [ ] Export functionality
- [ ] Data transformation features
- [ ] Machine learning integration
- [ ] Collaboration features

---

Built with ❤️ using React, Flask, and AI

