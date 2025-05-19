# Standard libraries
import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple

# LangChain core data structure for documents
from langchain_core.documents import Document

# Vector store client for AstraDB
from langchain_astradb import AstraDBVectorStore

# Utility to load embedding models
from utils.model_loader import ModelLoader

# YAML-based configuration loader
from config.config_loader import load_config

# DataIngestion Class Definition
class DataIngestion:
    """
    Class to handle data transformation and ingestion into AstraDB vector store.
    """

    # __init__ Constructor
    def __init__(self):
    # """
    # Initialize environment variables, embedding model, and set CSV file path.
    # """
        print("Initializing DataIngestion pipeline...")

        self.model_loader = ModelLoader()  # Load embedding model loader class
        self._load_env_variables()         # Load .env credentials for API keys
        self.csv_path = self._get_csv_path()  # Resolve path to product CSV file
        self.product_data = self._load_csv()  # Load the CSV as pandas DataFrame
        self.config = load_config()          # Load config.yaml as a dict


    # Load Environment Variables
    def _load_env_variables(self):
    # '''
    # Load and validate required environment variables.
    # '''
        
        
        load_dotenv()  # Load .env file into environment

        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]

        # Check for missing env vars
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

        # Save valid credentials to object variables
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")


       
    # Resolve CSV File Path
    def _get_csv_path(self):
        """
        Get path to the CSV file located inside 'data' folder.
        """
        current_dir = os.getcwd()  # Get current working directory
        csv_path = os.path.join(current_dir, 'data', 'flipkart_product_review.csv')

        # Raise error if CSV file not found
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        return csv_path

    # Load CSV with Product Data
    def _load_csv(self):
        """
        Load product data from CSV.
        """
        df = pd.read_csv(self.csv_path)  # Read CSV into pandas DataFrame
        expected_columns = {'product_title', 'rating', 'summary', 'review'}

        # Check if required columns exist
        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV must contain columns: {expected_columns}")

        return df

    # Transform CSV Data → LangChain Documents
    def transform_data(self):
        """
        Transform product data into list of LangChain Document objects.
        """
        product_list = []

        # Convert each row into a dictionary
        for _, row in self.product_data.iterrows():
            product_entry = {
                "product_name": row['product_title'],
                "product_rating": row['rating'],
                "product_summary": row['summary'],
                "product_review": row['review']
            }
            product_list.append(product_entry)

        # Convert each entry to a LangChain Document with metadata
        documents = []
        for entry in product_list:
            metadata = {
                "product_name": entry["product_name"],
                "product_rating": entry["product_rating"],
                "product_summary": entry["product_summary"]
            }
            doc = Document(page_content=entry["product_review"], metadata=metadata)
            documents.append(doc)

        print(f"Transformed {len(documents)} documents.")
        return documents


    # Store Embeddings into AstraDB
    def store_in_vector_db(self, documents: List[Document]):
        """
        Store documents into AstraDB vector store.
        """
        collection_name=self.config["astra_db"]["collection_name"]  # Get collection name from config.yaml

        # Initialize AstraDB vector store with embedding model
        vstore = AstraDBVectorStore(
            embedding= self.model_loader.load_embeddings(), # Load embedding model dynamically
            collection_name=collection_name,
            api_endpoint=self.db_api_endpoint,
            token=self.db_application_token,
            namespace=self.db_keyspace,
        )

        inserted_ids = vstore.add_documents(documents)  # Store documents in AstraDB
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids


    # Full Pipeline Runner
    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform_data()  # Step 1: CSV → LangChain Documents
        vstore, inserted_ids = self.store_in_vector_db(documents)  # Step 2: Store in vector DB

        # Optional: Run a quick similarity search
        query = "Can you tell me the low budget headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")

# CLI Entry Point
# Run if this file is executed directly
if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run_pipeline()


"""
Summary — Why You Wrote This:
Part	Purpose
✅ Class-based design-->	Makes it modular, testable, and reusable
✅ .env loading-->	Keeps secrets out of codebase
✅ config.yaml--> usage	Externalizes parameters (cleaner + scalable)
✅ CSV ingestion-->	Reads structured Flipkart product reviews
✅ LangChain Document-->	Standard format for text + metadata
✅ AstraDB Vector Store-->	Stores embeddings for search/retrieval
✅ run_pipeline()-->	Automates everything end-to-end
✅ CLI support-->	Makes the file runnable independently
"""