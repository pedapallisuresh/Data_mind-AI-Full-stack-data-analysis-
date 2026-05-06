import duckdb
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration - Support multiple providers
def get_llm_client():
    """Get LLM client based on available API keys"""
    # Try OpenAI first
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        from openai import OpenAI
        return OpenAI(api_key=openai_key), 'openai'
    
    # Try Ollama (local)
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            return None, 'ollama'
    except:
        pass
    
    # Fallback to Tavily
    from openai import OpenAI
    return OpenAI(api_key=os.getenv('TAVILY_API_KEY'), base_url="https://api.tavily.com/v1"), 'tavily'

def query_llm(prompt, system_prompt="You are a SQL expert.", model="gpt-3.5-turbo"):
    """Query LLM with fallback support"""
    client, provider = get_llm_client()
    
    if provider == 'openai':
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "invalid_api_key" in error_msg.lower():
                return "Error: Invalid or missing OpenAI API key. Please check your .env file and ensure OPENAI_API_KEY is set correctly."
            return f"OpenAI Error: {error_msg}"
    
    elif provider == 'ollama':
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"System: {system_prompt}\n\nUser: {prompt}",
                    "stream": False
                },
                timeout=60
            )
            return response.json().get('response', '').strip()
        except Exception as e:
            return f"Ollama Error: {str(e)}"
    
    else:  # tavily
        try:
            response = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Tavily Error: {str(e)}"

def query_together(prompt, retries=3):
    """Legacy function - uses query_llm instead"""
    return query_llm(prompt)


def run_query(df, question):
    if df is None or df.empty:
        return "Error", "No data available"

    con = None
    try:
        con = duckdb.connect()
        con.register("data", df)

        prompt = f"""
You are a SQL expert.

STRICT RULES:
- Use only table name: data
- Return ONLY SQL query
- No explanations
- No markdown
- No comments

Question: {question}
"""

        output = query_together(prompt)

        # Basic validation: check for SELECT
        if not output.upper().startswith("SELECT"):
            return output, "Generated query is not a valid SELECT statement"

        sql_query = output

        result_df = con.execute(sql_query).df()
        return sql_query, result_df

    except KeyError as e:
        return "Error", f"API Response Error: {str(e)}"
    except requests.RequestException as e:
        return "Error", f"API Request Error: {str(e)}"
    except Exception as e:
        return "Error", f"Unexpected Error: {str(e)}"
    finally:
        if con:
            con.close()
