from typing import List, Dict, Any
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    PythonCodeTextSplitter
)

class TextSplitterService:
    def __init__(self):
        self.splitter_types = {
            'recursive': RecursiveCharacterTextSplitter,
            'character': CharacterTextSplitter,
            'token': TokenTextSplitter,
            'markdown': MarkdownHeaderTextSplitter,
            'python': PythonCodeTextSplitter
        }
    
    def split_text(self, text: str, params: Dict[str, Any]) -> List[str]:
        """
        Split text using specified parameters
        
        Args:
            text: Text content to split
            params: Dictionary containing splitter configuration
                - splitter_type: Type of splitter ('recursive', 'character', 'token', etc.)
                - chunk_size: Size of each chunk (default: 1000)
                - chunk_overlap: Overlap between chunks (default: 200)
                - separators: Custom separators (optional)
                - keep_separator: Whether to keep separators (default: True)
        
        Returns:
            List of text chunks
        """
        # Default parameters
        splitter_type = params.get('splitter_type', 'recursive')
        chunk_size = params.get('chunk_size', 1000)
        chunk_overlap = params.get('chunk_overlap', 200)
        separators = params.get('separators', None)
        keep_separator = params.get('keep_separator', True)
        
        # Handle special cases
        if splitter_type == 'markdown':
            return self._split_markdown(text, params)
        elif splitter_type in ['python', 'javascript']:
            return self._split_code(text, splitter_type, params)
        
        # Standard text splitters
        splitter_class = self.splitter_types.get(splitter_type, RecursiveCharacterTextSplitter)
        
        # Build splitter arguments
        splitter_args = {
            'chunk_size': chunk_size,
            'chunk_overlap': chunk_overlap,
            'keep_separator': keep_separator
        }
        
        # Add separators if provided and supported
        if separators and splitter_type in ['recursive', 'character']:
            splitter_args['separators'] = separators
        
        # Remove unsupported arguments for token splitter
        if splitter_type == 'token':
            splitter_args.pop('keep_separator', None)
            splitter_args.pop('separators', None)
        
        try:
            splitter = splitter_class(**splitter_args)
            chunks = splitter.split_text(text)
            return [chunk.strip() for chunk in chunks if chunk.strip()]
        except Exception as e:
            # Fallback to basic recursive splitter
            fallback_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            chunks = fallback_splitter.split_text(text)
            return [chunk.strip() for chunk in chunks if chunk.strip()]
    
    def _split_markdown(self, text: str, params: Dict[str, Any]) -> List[str]:
        """Split markdown text by headers"""
        headers_to_split_on = params.get('headers_to_split_on', [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ])
        
        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        
        try:
            md_docs = md_splitter.split_text(text)
            chunks = []
            
            for doc in md_docs:
                content = doc.page_content.strip()
                if content:
                    # Add metadata as context if available
                    if hasattr(doc, 'metadata') and doc.metadata:
                        header_info = " | ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
                        content = f"[{header_info}]\n\n{content}"
                    chunks.append(content)
            
            return chunks if chunks else [text]
        except:
            # Fallback to regular splitting
            return self.split_text(text, {**params, 'splitter_type': 'recursive'})
    
    def _split_code(self, text: str, language: str, params: Dict[str, Any]) -> List[str]:
        """Split code by language-specific rules"""
        chunk_size = params.get('chunk_size', 1000)
        chunk_overlap = params.get('chunk_overlap', 200)
        
        if language == 'python':
            splitter = PythonCodeTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        elif language == 'javascript':
            # Use RecursiveCharacterTextSplitter with JS-specific separators
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=['\nfunction ', '\nclass ', '\nconst ', '\nlet ', '\nvar ', '\n\n', '\n', ' ', '']
            )
        else:
            # Fallback
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
        
        try:
            chunks = splitter.split_text(text)
            return [chunk.strip() for chunk in chunks if chunk.strip()]
        except:
            # Fallback to regular splitting
            return self.split_text(text, {**params, 'splitter_type': 'recursive'})
    
    def get_splitter_info(self) -> Dict[str, Any]:
        """Get information about available splitters and their parameters"""
        return {
            'splitter_types': {
                'recursive': {
                    'description': 'Recursively splits text using multiple separators',
                    'parameters': ['chunk_size', 'chunk_overlap', 'separators', 'keep_separator'],
                    'default_separators': ['\\n\\n', '\\n', ' ', '']
                },
                'character': {
                    'description': 'Splits text by a single separator',
                    'parameters': ['chunk_size', 'chunk_overlap', 'separators', 'keep_separator'],
                    'default_separators': ['\\n\\n']
                },
                'token': {
                    'description': 'Splits text by token count',
                    'parameters': ['chunk_size', 'chunk_overlap']
                },
                'markdown': {
                    'description': 'Splits markdown by headers',
                    'parameters': ['headers_to_split_on']
                },
                'python': {
                    'description': 'Splits Python code by functions/classes',
                    'parameters': ['chunk_size', 'chunk_overlap']
                },
                'javascript': {
                    'description': 'Splits JavaScript code by functions/declarations',
                    'parameters': ['chunk_size', 'chunk_overlap']
                }
            },
            'default_params': {
                'chunk_size': 1000,
                'chunk_overlap': 200,
                'keep_separator': True
            }
        }
