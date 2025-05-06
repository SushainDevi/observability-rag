import duckdb
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

class ObservabilityAssistant:
    def __init__(self):
        # Initialize DuckDB connection
        self.conn = duckdb.connect('observability.db')
        
        # Initialize Llama3 via Ollama
        self.llm = ChatOllama(
            model="llama3.2:1b",
            temperature=0.3,  # More deterministic outputs
            num_ctx=4096,     # Larger context window
            top_k=40          # Better for factual queries
        )
        
        # Modify the SQL prompt template
        self.sql_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at converting observability queries to DuckDB SQL.
            Database Schema:
            Table: telemetry
            - server_id (TEXT): Server identifier (use this instead of 'host')
            - metric_name (TEXT): 'cpu', 'memory', or 'disk'
            - metric_value (FLOAT): Percentage value (0-100)
            - timestamp (TIMESTAMP)
            
            Conversion Rules:
            1. Always use 'server_id' column for server identification
            2. For time ranges, use: timestamp >= NOW() - INTERVAL 'X hours'
            3. Handle percentages as direct comparisons (65% = 65.0)
            
            Example Conversions:
            User: List hosts with disk >90% today
            SQL: SELECT DISTINCT server_id FROM telemetry 
                  WHERE metric_name = 'disk' 
                  AND metric_value > 90.0 
                  AND timestamp >= date_trunc('day', NOW())
            
            User: Show servers with CPU spikes last hour
            SQL: SELECT server_id FROM telemetry 
                  WHERE metric_name = 'cpu' 
                  AND metric_value > 80.0 
                  AND timestamp >= NOW() - INTERVAL '1 hour'
            
            Respond ONLY with valid SQL."""),
            ("human", "{query}")
        ])
        
        # Improved response template
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", """Transform SQL results into professional observability alerts.
            Rules:
            - Highlight critical values (>90%) with ❗
            - Format timestamps clearly
            - Summarize when >5 results
            
            Query: {query}
            Results: {results}
            
            Example:
            "3 servers exceeded memory thresholds:
            • server_01 (92% ❗ at 14:30)
            • server_02 (87% at 15:10)"
            """),
            ("human", "Generate concise report:")
        ])

    def generate_sql(self, query):
        chain = self.sql_prompt | self.llm
        return chain.invoke({"query": query}).content.strip()

    def execute_query(self, sql):
        try:
            result = self.conn.execute(sql)
            if result is None:
                return "No results found"
            return result.df()
        except Exception as e:
            print(f"SQL Error: {str(e)}")  # Log full error
            return f"SQL Error: Please rephrase your query. Common issues:\n- Use 'server' instead of 'host'\n- Check time range formatting\n- Verify metric names (cpu/memory/disk)"

    def generate_response(self, query, results):
        if isinstance(results, str) and "SQL Error" in results:
            return f"❌ **Validation Error**\n{results}"
        
        # Convert DataFrame to readable string
        results_str = results.to_markdown(index=False) if hasattr(results, 'to_markdown') else str(results)
        
        chain = self.response_prompt | self.llm
        return chain.invoke({
            "query": query,
            "results": results_str
        }).content

    def process_query(self, query):
        try:
            print(f"\nProcessing: {query}")
            sql = self.generate_sql(query)
            print(f"Generated SQL:\n{sql}")
            
            results = self.execute_query(sql)
            response = self.generate_response(query, results)
            
            return f"\n🔍 Results:\n{response}"
        except Exception as e:
            return f"\n⚠️ Error: {str(e)}"