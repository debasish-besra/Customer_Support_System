import yaml  # Importing the PyYAML library to read and parse YAML files

def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Loads the configuration settings from a YAML file and returns it as a Python dictionary.
    
    Parameters:
    config_path (str): Path to the YAML config file (default is 'config/config.yaml').

    Returns:
    dict: Configuration parameters as a dictionary.
    """
    
    # Open the YAML configuration file in read mode
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)  # Parse the YAML content into a Python dictionary

    return config  # Return the parsed config dictionary for use throughout the project


'''
Great! You've written a config_loader.py utility to cleanly and consistently load your configuration settings from the config.yaml file. This makes your codebase more modular, reusable, and scalable — especially important in GenAI/LLM applications.

Why You Wrote This Function
You created this utility function to:
Avoid duplicating code every time you need to load settings from config.yaml.
Standardize how configurations are loaded across multiple Python files/modules (e.g., data ingestion, chatbot setup, vector store initialization).
Make your code cleaner and more maintainable, especially in team or production settings.
Allow you to easily swap config files later by just changing config_path.

'''