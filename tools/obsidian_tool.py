import os
import logging
from typing import Optional

class ObsidianLoader:
    """
    Handles reading and searching within an Obsidian vault.
    """
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.logger = logging.getLogger(__name__)

    def search_vault(self, query: str) -> str:
        """
        Searches for files containing the query in the vault.
        """
        if not os.path.exists(self.vault_path):
            return f"Error: Vault path '{self.vault_path}' does not exist."

        results = []
        for root, _, files in os.walk(self.vault_path):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                results.append(f"--- {file} ---\n{content[:500]}...")
                    except:
                        pass
        
        if not results:
            return f"No results found for '{query}' in the vault."
        
        return "\n\n".join(results[:3]) # Limit to top 3 matches for context

def create_obsidian_tool(vault_path: str):
    """
    Helper function to create a LangChain tool for Obsidian.
    """
    loader = ObsidianLoader(vault_path)
    
    def run_obsidian_search(query: str) -> str:
        return loader.search_vault(query)
        
    return {
        "name": "obsidian_search",
        "description": "Searches for information within the user's private Obsidian notes and knowledge base.",
        "func": run_obsidian_search
    }
