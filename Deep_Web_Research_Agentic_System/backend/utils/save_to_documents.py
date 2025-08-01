import os
import datetime
from backend.exception.exception import CustomException
from backend.logger.logger import CustomLogger

logger = CustomLogger().get_logger()

def save_document(response_text: str, directory: str = None) -> str:
    """Export AI-generated content to Markdown file with proper formatting."""

    try:
        if directory is None:  # Dynamically calculate the correct directory path if not provided
            directory = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "save_to_documents")
            )

        os.makedirs(directory, exist_ok=True)
        markdown_content = f"""# Deep Web Research Response

**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}  
**Created by:** Atriyo's Deep Web Research Agentic System

---

{response_text}

---

*This content was generated by an AI-powered agent. Always cross-check facts, citations, and source reliability before using it in critical research or publication.*
"""

        # Create filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(directory, f"Deep_Web_Research_Response_{timestamp}.md")

        # Write markdown to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        logger.info(f"Markdown file saved as: {filename}")
        return filename

    except Exception as e:
        logger.error(f"Error saving markdown file: {e}")
        raise CustomException("Failed to save document.") from e
