from rag_core import ObservabilityAssistant

def main():
    assistant = ObservabilityAssistant()
    print("Observability Assistant (type 'exit' to quit)")
    
    while True:
        query = input("\nQuery: ")
        if query.lower() == 'exit':
            break
        response = assistant.process_query(query)
        print(f"\nResponse: {response}")

if __name__ == "__main__":
    main()