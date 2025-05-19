# Import the config loader function from the config directory
from config.config_loader import load_config

# Load the entire configuration from the YAML file as a Python dictionary
config = load_config()

# Access specific configuration values using dictionary keys
collection_name = config["astra_db"]["collection_name"]  # Name of the Astra DB collection for storing/retrieving vectors
embedding_model_name = config["embedding_model"]["model_name"]  # The model used to convert text into embeddings
top_k = config["retriever"]["top_k"]  # Number of top similar results to return in a similarity search

# Print out the loaded values to verify they are being loaded correctly
print(collection_name)
print(embedding_model_name)
print(top_k)



'''
Your test.py file is a configuration check script that ensures your config.yaml is correctly set up and loaded via config_loader.py

Why You Wrote This
You created test.py to:
✅ Test whether config.yaml loads correctly with the load_config() function.
✅ Verify individual fields like collection_name, model_name, and top_k are accessible and accurate.
✅ Catch early bugs or typos in your YAML file or config loading logic before you run more complex parts of the app.
✅ Use it as a reference when integrating these configs into other parts of your project (like ingestion, chatbot, etc.).

'''