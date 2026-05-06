from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
import json
import requests
import sqlite3
from analyzer import (
    generate_summary,
    generate_descriptive_stats,
    generate_comprehensive_analysis,
    generate_ai_insights,
    generate_data_profiling,
    generate_visualization_suggestions,
    generate_statistical_summary,
    generate_comprehensive_agent_analysis
)
from cleaner import clean_data
from qa_engine import run_query

app = Flask(__name__)
CORS(app)

# Store data in memory - Support for multiple datasets
import uuid

data_store = {
    'datasets': {},  # Dictionary to store multiple datasets: {dataset_id: {df, cleaned_df, source_type, source_info, name, created_at}}
    'active_dataset_id': None  # Currently active dataset
}

def generate_dataset_id():
    """Generate a unique ID for each dataset"""
    return str(uuid.uuid4())[:8]

def get_active_dataset():
    """Get the currently active dataset"""
    if data_store['active_dataset_id'] and data_store['active_dataset_id'] in data_store['datasets']:
        return data_store['datasets'][data_store['active_dataset_id']]
    return None

def set_active_dataset(dataset_id):
    """Set the active dataset"""
    if dataset_id in data_store['datasets']:
        data_store['active_dataset_id'] = dataset_id
        return True
    return False

# Helper function to load data from various sources - Updated for multi-dataset support
def load_data_to_store(df, source_type, source_info=None, name=None):
    """Load data into the store and return preview"""
    import time
    
    dataset_id = generate_dataset_id()
    dataset_name = name or source_info or f"Dataset {len(data_store['datasets']) + 1}" if source_info else f"Dataset {len(data_store['datasets']) + 1}"
    
    data_store['datasets'][dataset_id] = {
        'df': df,
        'cleaned_df': None,
        'source_type': source_type,
        'source_info': source_info,
        'name': dataset_name,
        'created_at': time.time()
    }
    data_store['active_dataset_id'] = dataset_id
    
    return {
        'dataset_id': dataset_id,
        'preview': df.head(100).to_dict(orient='records'),
        'columns': list(df.columns),
        'shape': df.shape
    }

# Updated helper to get current DataFrame
def get_current_df():
    """Get the current dataset's DataFrame"""
    if data_store['active_dataset_id'] and data_store['active_dataset_id'] in data_store['datasets']:
        ds = data_store['datasets'][data_store['active_dataset_id']]
        return ds['cleaned_df'] if ds['cleaned_df'] is not None else ds['df']
    return None

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        df = pd.read_csv(file)
        name = file.filename.rsplit('.', 1)[0] if file.filename else 'Untitled'
        
        result = load_data_to_store(df, 'file', file.filename, name)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'dataset_id': result['dataset_id'],
            'preview': result['preview'],
            'columns': result['columns'],
            'shape': result['shape']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summary', methods=['GET'])
def get_summary():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        summary = generate_summary(df)
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clean', methods=['POST'])
def clean():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        if data_store['active_dataset_id']:
            data_store['datasets'][data_store['active_dataset_id']]['cleaned_df'] = clean_data(df.copy())
            cleaned_df = data_store['datasets'][data_store['active_dataset_id']]['cleaned_df']
        
        return jsonify({
            'message': 'Data cleaned successfully',
            'preview': cleaned_df.head(100).to_dict(orient='records'),
            'shape': cleaned_df.shape
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comprehensive-analysis', methods=['GET'])
def comprehensive_analysis():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        analysis = generate_comprehensive_analysis(df)
        
        # Convert numpy types to Python types for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(i) for i in obj]
            elif hasattr(obj, 'item'):  # numpy types
                return obj.item()
            elif hasattr(obj, 'tolist'):  # numpy arrays
                return obj.tolist()
            else:
                return obj
        
        return jsonify(convert_to_serializable(analysis))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai-insights', methods=['GET'])
def ai_insights():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        insights = generate_ai_insights(df)
        return jsonify({'insights': insights})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/data-profiling', methods=['GET'])
def data_profiling():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        profiling = generate_data_profiling(df)
        
        # Convert numpy types
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(i) for i in obj]
            elif hasattr(obj, 'item'):
                return obj.item()
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            else:
                return obj
        
        return jsonify(convert_to_serializable(profiling))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/visualization-suggestions', methods=['GET'])
def visualization_suggestions():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        suggestions = generate_visualization_suggestions(df)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/statistical-summary', methods=['GET'])
def statistical_summary():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        stats = generate_statistical_summary(df)
        
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(i) for i in obj]
            elif hasattr(obj, 'item'):
                return obj.item()
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            else:
                return obj
        
        return jsonify(convert_to_serializable(stats))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/comprehensive-agent-analysis', methods=['GET'])
def comprehensive_agent_analysis():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        analysis = generate_comprehensive_agent_analysis(df)
        
        def convert_to_serializable(obj):
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_to_serializable(i) for i in obj]
            elif hasattr(obj, 'item'):
                return obj.item()
            elif hasattr(obj, 'tolist'):
                return obj.tolist()
            else:
                return obj
        
        return jsonify(convert_to_serializable(analysis))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def query():
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        sql, answer = run_query(df, question)
        
        if isinstance(answer, str):
            return jsonify({'error': answer, 'sql': sql})
        
        return jsonify({
            'sql': sql,
            'result': answer.head(100).to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/agent-chat', methods=['POST'])
def agent_chat():
    """Conversational AI agent for data analysis"""
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        data = request.json
        message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get data summary for context
        summary = generate_summary(df)
        desc_stats = generate_descriptive_stats(df)
        
        # Build conversation context
        context = f"""
Current Dataset:
- Rows: {summary['Total Rows']}, Columns: {summary['Total Columns']}
- Column Names: {', '.join(summary['Column Names'])}
- Data Types: {summary['Data Types']}

Sample Data (first 5 rows):
{df.head().to_string()}

Descriptive Statistics:
{str(desc_stats)}

You are a data analysis assistant. Answer the user's question based on the data above.
Be specific and refer to actual data values when possible.
"""
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": "You are a helpful data analysis assistant. Use the provided data context to answer questions accurately."}
        ]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append(msg)
        
        # Add context and current message
        messages.append({"role": "user", "content": f"{context}\n\nUser Question: {message}"})
        
        # Get response from LLM
        from analyzer import query_llm
        response = query_llm(
            prompt=f"{context}\n\nUser Question: {message}",
            system_prompt="You are a helpful data analysis assistant. Use the provided data context to answer questions accurately. Provide specific insights based on the data.",
            model="gpt-3.5-turbo"
        )
        
        return jsonify({
            'response': response,
            'context': {
                'rows': summary['Total Rows'],
                'columns': summary['Total Columns']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['GET'])
def preview():
    try:
        if data_store['df'] is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        df = data_store['cleaned_df'] if data_store['cleaned_df'] is not None else data_store['df']
        return jsonify({
            'preview': df.head(100).to_dict(orient='records'),
            'columns': list(df.columns),
            'shape': df.shape,
            'source_type': data_store['source_type'],
            'source_info': data_store['source_info']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ======= New Data Source Endpoints =======

@app.route('/upload/url', methods=['POST'])
def upload_from_url():
    """Load data from a URL (CSV, JSON, Excel)"""
    try:
        data = request.json
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Determine file type from URL
        url_lower = url.lower()
        
        # Disable SSL verification for requests (for Windows compatibility)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        if url_lower.endswith('.csv'):
            df = pd.read_csv(url)
        elif url_lower.endswith('.json'):
            df = pd.read_json(url)
        elif url_lower.endswith('.xlsx') or url_lower.endswith('.xls'):
            df = pd.read_excel(url)
        elif url_lower.endswith('.parquet'):
            df = pd.read_parquet(url)
        else:
            # Try to detect format
            response = requests.get(url, timeout=30, verify=False)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            
            if 'csv' in content_type:
                df = pd.read_csv(io.StringIO(response.text))
            elif 'json' in content_type:
                df = pd.read_json(response.text)
            else:
                # Try CSV by default
                df = pd.read_csv(io.StringIO(response.text))
        
        result = load_data_to_store(df, 'url', url)
        
        return jsonify({
            'message': 'Data loaded from URL successfully',
            **result
        })
    except requests.RequestException as e:
        return jsonify({'error': f'Error fetching URL: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload/api', methods=['POST'])
def upload_from_api():
    """Load data from an API endpoint"""
    try:
        data = request.json
        api_url = data.get('api_url', '')
        headers = data.get('headers', {})
        params = data.get('params', {})
        
        if not api_url:
            return jsonify({'error': 'No API URL provided'}), 400
        
        # Make request to API (disable SSL verification for Windows)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(api_url, headers=headers, params=params, timeout=30, verify=False)
        response.raise_for_status()
        
        # Try to parse response
        content_type = response.headers.get('Content-Type', '')
        
        if 'json' in content_type:
            json_data = response.json()
            
            # Handle different JSON structures
            if isinstance(json_data, list):
                df = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # Check for common data keys
                for key in ['data', 'results', 'items', 'records', 'rows']:
                    if key in json_data and isinstance(json_data[key], list):
                        df = pd.DataFrame(json_data[key])
                        break
                else:
                    # If no common key found, use the whole dict
                    df = pd.DataFrame([json_data])
            else:
                return jsonify({'error': 'Unsupported response format'}), 400
        elif 'csv' in content_type:
            df = pd.read_csv(io.StringIO(response.text))
        else:
            return jsonify({'error': 'Unsupported content type'}), 400
        
        result = load_data_to_store(df, 'api', api_url)
        
        return jsonify({
            'message': 'Data loaded from API successfully',
            **result
        })
    except requests.RequestException as e:
        return jsonify({'error': f'Error fetching from API: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload/database', methods=['POST'])
def upload_from_database():
    """Load data from a SQL database"""
    try:
        data = request.json
        db_type = data.get('db_type', 'sqlite')  # sqlite, postgresql, mysql
        connection_string = data.get('connection_string', '')
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No SQL query provided'}), 400
        
        if db_type == 'sqlite':
            # For SQLite, connection_string is the file path
            conn = sqlite3.connect(connection_string if connection_string else ':memory:')
            df = pd.read_sql(query, conn)
            conn.close()
            source_info = connection_string if connection_string else 'In-memory SQLite'
        elif db_type == 'postgresql':
            if not connection_string:
                return jsonify({'error': 'Connection string required for PostgreSQL'}), 400
            df = pd.read_sql(query, connection_string)
            source_info = connection_string
        elif db_type == 'mysql':
            if not connection_string:
                return jsonify({'error': 'Connection string required for MySQL'}), 400
            df = pd.read_sql(query, connection_string)
            source_info = connection_string
        else:
            return jsonify({'error': f'Unsupported database type: {db_type}'}), 400
        
        result = load_data_to_store(df, 'database', source_info)
        
        return jsonify({
            'message': 'Data loaded from database successfully',
            **result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload/pipeline', methods=['POST'])
def upload_from_pipeline():
    """Load data from a data pipeline (custom pipeline)"""
    try:
        data = request.json
        pipeline_type = data.get('pipeline_type', '')
        config = data.get('config', {})
        
        if not pipeline_type:
            return jsonify({'error': 'No pipeline type specified'}), 400
        
        df = None
        source_info = pipeline_type
        
        # Custom pipeline implementations
        if pipeline_type == 'snowflake':
            # Snowflake configuration
            account = config.get('account', '')
            user = config.get('user', '')
            password = config.get('password', '')
            warehouse = config.get('warehouse', '')
            database = config.get('database', '')
            schema = config.get('schema', '')
            query = config.get('query', '')
            
            if not all([account, user, password, query]):
                return jsonify({'error': 'Missing Snowflake configuration'}), 400
            
            # Build connection string
            conn_str = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"
            df = pd.read_sql(query, conn_str)
            
        elif pipeline_type == 'bigquery':
            # Google BigQuery
            project_id = config.get('project_id', '')
            dataset = config.get('dataset', '')
            table = config.get('table', '')
            
            if not all([project_id, dataset, table]):
                return jsonify({'error': 'Missing BigQuery configuration'}), 400
            
            # Use google-cloud-bigquery (would need to be installed)
            try:
                from google.cloud import bigquery
                client = bigquery.Client(project=project_id)
                query = f"SELECT * FROM `{project_id}.{dataset}.{table}`"
                df = client.query(query).to_dataframe()
            except ImportError:
                return jsonify({'error': 'google-cloud-bigquery not installed'}), 500
            
        elif pipeline_type == 'databricks':
            # Databricks
            server_hostname = config.get('server_hostname', '')
            http_path = config.get('http_path', '')
            access_token = config.get('access_token', '')
            query = config.get('query', '')
            
            if not all([server_hostname, http_path, access_token, query]):
                return jsonify({'error': 'Missing Databricks configuration'}), 400
            
            from databricks import sql
            with sql.connect(server_hostname=server_hostname, http_path=http_path, access_token=access_token) as conn:
                df = conn.sql(query).fetchall()
                df = pd.DataFrame(df)
            
        elif pipeline_type == 'kafka':
            # Kafka streaming data (simulated as sample)
            # In production, this would connect to Kafka and consume messages
            bootstrap_servers = config.get('bootstrap_servers', 'localhost:9092')
            topic = config.get('topic', '')
            
            if not topic:
                return jsonify({'error': 'Kafka topic required'}), 400
            
            # Placeholder - would need kafka-python library
            return jsonify({'error': 'Kafka pipeline requires additional setup'}), 500
            
        elif pipeline_type == 'airtable':
            # Airtable API
            api_key = config.get('api_key', '')
            base_id = config.get('base_id', '')
            table_name = config.get('table_name', '')
            
            if not all([api_key, base_id, table_name]):
                return jsonify({'error': 'Missing Airtable configuration'}), 400
            
            url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
            headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            records = response.json().get('records', [])
            df = pd.DataFrame([r.get('fields', {}) for r in records])
            
        elif pipeline_type == 'google_sheets':
            # Google Sheets
            sheet_id = config.get('sheet_id', '')
            sheet_name = config.get('sheet_name', '')
            
            if not sheet_id:
                return jsonify({'error': 'Google Sheet ID required'}), 400
            
            url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
            if sheet_name:
                url += f"&sheet={sheet_name}"
            
            df = pd.read_csv(url)
            
        elif pipeline_type == 'custom':
            # Custom Python code execution (sandboxed)
            code = config.get('code', '')
            
            if not code:
                return jsonify({'error': 'No custom code provided'}), 400
            
            # This is a security risk in production - would need proper sandboxing
            return jsonify({'error': 'Custom pipeline requires secure execution environment'}), 500
        else:
            return jsonify({'error': f'Unsupported pipeline type: {pipeline_type}'}), 400
        
        if df is None or df.empty:
            return jsonify({'error': 'No data returned from pipeline'}), 400
        
        result = load_data_to_store(df, 'pipeline', source_info)
        
        return jsonify({
            'message': f'Data loaded from {pipeline_type} pipeline successfully',
            **result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/source-info', methods=['GET'])
def get_source_info():
    """Get information about the current data source"""
    try:
        if data_store['active_dataset_id'] is None:
            return jsonify({'error': 'No data loaded'}), 400
        
        ds = data_store['datasets'][data_store['active_dataset_id']]
        return jsonify({
            'source_type': ds['source_type'],
            'source_info': ds['source_info']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ======= Multi-Dataset Management Endpoints =======

@app.route('/datasets', methods=['GET'])
def list_datasets():
    """List all datasets"""
    try:
        datasets_list = []
        for ds_id, ds_data in data_store['datasets'].items():
            datasets_list.append({
                'id': ds_id,
                'name': ds_data['name'],
                'source_type': ds_data['source_type'],
                'source_info': ds_data['source_info'],
                'shape': ds_data['df'].shape,
                'created_at': ds_data['created_at'],
                'is_active': ds_id == data_store['active_dataset_id']
            })
        return jsonify({'datasets': datasets_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/datasets/switch', methods=['POST'])
def switch_dataset():
    """Switch to a different dataset"""
    try:
        data = request.json
        dataset_id = data.get('dataset_id')
        
        if not dataset_id:
            return jsonify({'error': 'No dataset_id provided'}), 400
        
        if dataset_id not in data_store['datasets']:
            return jsonify({'error': 'Dataset not found'}), 404
        
        data_store['active_dataset_id'] = dataset_id
        ds = data_store['datasets'][dataset_id]
        
        return jsonify({
            'message': f'Switched to dataset: {ds["name"]}',
            'preview': ds['df'].head(100).to_dict(orient='records'),
            'columns': list(ds['df'].columns),
            'shape': ds['df'].shape,
            'source_type': ds['source_type'],
            'source_info': ds['source_info'],
            'dataset_id': dataset_id,
            'dataset_name': ds['name']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/datasets/delete', methods=['POST'])
def delete_dataset():
    """Delete a dataset"""
    try:
        data = request.json
        dataset_id = data.get('dataset_id')
        
        if not dataset_id:
            return jsonify({'error': 'No dataset_id provided'}), 400
        
        if dataset_id not in data_store['datasets']:
            return jsonify({'error': 'Dataset not found'}), 404
        
        ds_name = data_store['datasets'][dataset_id]['name']
        del data_store['datasets'][dataset_id]
        
        # If we deleted the active dataset, switch to another one
        if data_store['active_dataset_id'] == dataset_id:
            if data_store['datasets']:
                data_store['active_dataset_id'] = list(data_store['datasets'].keys())[0]
            else:
                data_store['active_dataset_id'] = None
        
        return jsonify({'message': f'Deleted dataset: {ds_name}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ======= Visualization Data Endpoint =======

@app.route('/visualization-data', methods=['GET'])
def get_visualization_data():
    """Get data formatted for visualizations"""
    try:
        df = get_current_df()
        if df is None:
            return jsonify({'error': 'No data uploaded'}), 400
        
        import numpy as np
        
        viz_data = {
            'numeric_columns': [],
            'categorical_columns': [],
            'histogram_data': {},
            'bar_chart_data': {},
            'correlation_matrix': [],
            'box_plot_data': {}
        }
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        viz_data['numeric_columns'] = numeric_cols
        viz_data['categorical_columns'] = categorical_cols
        
        # Histogram data for numeric columns
        for col in numeric_cols[:5]:  # Limit to first 5
            hist, bin_edges = np.histogram(df[col].dropna(), bins=10)
            viz_data['histogram_data'][col] = {
                'bins': bin_edges[:-1].tolist(),
                'counts': hist.tolist()
            }
        
        # Bar chart data for categorical columns
        for col in categorical_cols[:5]:  # Limit to first 5
            value_counts = df[col].value_counts().head(10)
            viz_data['bar_chart_data'][col] = {
                'values': [str(v) for v in value_counts.index.tolist()],
                'counts': value_counts.values.tolist()
            }
        
        # Correlation matrix for numeric columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            viz_data['correlation_matrix'] = {
                'columns': numeric_cols,
                'matrix': corr_matrix.values.tolist()
            }
        
        # Box plot data for numeric columns
        for col in numeric_cols[:5]:  # Limit to first 5
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            median = df[col].median()
            min_val = df[col].min()
            max_val = df[col].max()
            
            viz_data['box_plot_data'][col] = {
                'min': float(min_val) if not np.isnan(min_val) else 0,
                'q1': float(q1) if not np.isnan(q1) else 0,
                'median': float(median) if not np.isnan(median) else 0,
                'q3': float(q3) if not np.isnan(q3) else 0,
                'max': float(max_val) if not np.isnan(max_val) else 0
            }
        
        return jsonify(viz_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

