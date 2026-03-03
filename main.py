from src.ingestion import ingest_contracts
from src.agents import rag_agent
 
 
def main():
    contracts_path = "data/contracts"
 
    print("Starting ingestion...")
    ingest_contracts(contracts_path)
    print("Ingestion completed.")
 
    while True:
        question = input("\nAsk a question (or type 'exit'): ")
 
        if question.lower() == "exit":
            break
 
        answer = rag_agent(question)
 
        print("\nAnswer:")
        print(answer)
 
 
if __name__ == "__main__":
    main()