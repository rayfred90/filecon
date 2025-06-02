from abc import ABC, abstractmethod
from typing import Any, Dict, Union

class BaseProcessor(ABC):
    """Base class for all document processors"""
    
    @abstractmethod
    def process(self, filepath: str) -> Union[str, Dict[str, Any]]:
        """Process a document and return its content"""
        pass
    
    def to_markdown(self, content: Union[str, Dict[str, Any]]) -> str:
        """Convert processed content to markdown format"""
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            return self._dict_to_markdown(content)
        else:
            return str(content)
    
    def _dict_to_markdown(self, data: Dict[str, Any], level: int = 1) -> str:
        """Convert dictionary to markdown format"""
        markdown = ""
        
        for key, value in data.items():
            header = "#" * min(level, 6)
            markdown += f"{header} {key}\n\n"
            
            if isinstance(value, dict):
                markdown += self._dict_to_markdown(value, level + 1)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        markdown += f"### Item {i + 1}\n\n"
                        markdown += self._dict_to_markdown(item, level + 2)
                    else:
                        markdown += f"- {item}\n"
                markdown += "\n"
            else:
                markdown += f"{value}\n\n"
        
        return markdown
