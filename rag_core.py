import duckdb
import json
from transformers import pipeline, AutoModel, AutoTokenizer
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel

class QueryIntent(BaseModel):
    metric: str
    threshold: float
    timeframe: str
    servers: list[str]

class ObservabilityAssistant:
    def __init__(self):
        # Initialize components
        self.conn = duckdb.connect('observability.db')
        self.embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.intent_classifier = pipeline(
            "text-classification", 
            model="typeform/distilbert-base-uncased-mnli"
        )
        self.vector_store = self._init_vector_store()
        
        # Quantized model for SQL generation
        self.sql_model = AutoModel.from_pretrained(
            "tscholak/codegen-sql-350m-multi",
            device_map="auto",
            load_in_4bit=True
        )
        self.sql_tokenizer = AutoTokenizer.from_pretrained("tscholak/codegen-sql-350m-multi")

    def _init_vector_store(self):
        # Initialize with sample query patterns
        example_queries = [
            "cpu usage over 80% last hour",
            "memory consumption above 90% today",
            "disk space exceeding 85% past 24 hours"
        ]
        return FAISS.from_texts(example_queries, self.embedder)

    def _parse_intent(self, query: str) -> QueryIntent:
        # Structured output using model
        template = """Extract:
        { "metric": "cpu|memory|disk", 
        "threshold": number,
        "timeframe": "duration", 
        "servers": [] }"""
        
        result = self.intent_classifier(query, candidate_labels=["cpu", "memory", "disk"])
        return QueryIntent(
            metric=result["labels"][0],
            threshold=self._extract_threshold(query),
            timeframe=self._extract_timeframe(query),
            servers=[]
        )

    def _retrieve_similar_queries(self, query: str, k=3) -> list:
        return self.vector_store.similarity_search(query, k=k)

    def generate_sql(self, query: str) -> str:
        # Retrieve contextual examples
        examples = [doc.page_content for doc in self._retrieve_similar_queries(query)]
        
        # Generate SQL using fine-tuned model
        inputs = self.sql_tokenizer.encode(
            f"Query: {query}\nExamples: {examples}\nSQL:",
            return_tensors="pt"
        )
        outputs = self.sql_model.generate(inputs, max_length=200)
        return self.sql_tokenizer.decode(outputs[0], skip_special_tokens=True)

    def _validate_sql(self, sql: str) -> bool:
        try:
            self.conn.execute(f"EXPLAIN {sql}")
            return True
        except:
            return False

    def execute_query(self, sql: str):
        if not self._validate_sql(sql):
            raise ValueError("Invalid SQL query")
        return self.conn.execute(sql).df()

    def generate_response(self, results) -> str:
        # Structured templating instead of LLM formatting
        if not isinstance(results, pd.DataFrame):
            return results
        
        response = ["Analysis Results:"]
        for _, row in results.iterrows():
            alert = "❗" if row['metric_value'] > 90 else ""
            response.append(
                f"{row['server_id']}: {row['metric_value']}% {alert}"
            )
        return "\n".join(response)

    def process_query(self, query: str):
        try:
            # Structured intent parsing
            intent = self._parse_intent(query)
            
            # SQL generation with model + context
            sql = self.generate_sql(query)
            
            # Execute and format
            results = self.execute_query(sql)
            return self.generate_response(results)
            
        except Exception as e:
            return f"Error: {str(e)}"
