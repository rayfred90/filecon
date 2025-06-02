import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import Dict, Any
from .base_processor import BaseProcessor

class EbookProcessor(BaseProcessor):
    """Process EPUB and MOBI files"""
    
    def process(self, filepath: str) -> Dict[str, Any]:
        """Extract text from ebook files"""
        result = {
            'text': '',
            'chapters': [],
            'metadata': {}
        }
        
        try:
            file_extension = filepath.split('.')[-1].lower()
            
            if file_extension == 'epub':
                result = self._process_epub(filepath)
            elif file_extension == 'mobi':
                # For MOBI files, we'll need a different approach
                # For now, return an error message
                result['error'] = "MOBI format requires additional dependencies. Please convert to EPUB first."
                result['text'] = "MOBI format processing not fully implemented yet."
            
        except Exception as e:
            result['error'] = str(e)
            result['text'] = f"Error processing ebook: {str(e)}"
        
        return result
    
    def _process_epub(self, filepath: str) -> Dict[str, Any]:
        """Process EPUB file"""
        result = {
            'text': '',
            'chapters': [],
            'metadata': {}
        }
        
        try:
            book = epub.read_epub(filepath)
            
            # Extract metadata
            result['metadata'] = {
                'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else '',
                'author': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else '',
                'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else '',
                'publisher': book.get_metadata('DC', 'publisher')[0][0] if book.get_metadata('DC', 'publisher') else '',
                'description': book.get_metadata('DC', 'description')[0][0] if book.get_metadata('DC', 'description') else ''
            }
            
            text_parts = []
            
            # Add metadata section
            if result['metadata']['title']:
                text_parts.append(f"# {result['metadata']['title']}\n")
            if result['metadata']['author']:
                text_parts.append(f"**Author:** {result['metadata']['author']}\n")
            text_parts.append("\n---\n\n")
            
            chapter_num = 1
            
            # Extract text from each item
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content()
                    
                    # Parse HTML content
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text
                    text = soup.get_text()
                    
                    # Clean up text
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    if text.strip():
                        chapter_data = {
                            'chapter_number': chapter_num,
                            'title': item.get_name(),
                            'content': text.strip()
                        }
                        
                        result['chapters'].append(chapter_data)
                        
                        # Add to main text
                        text_parts.append(f"## Chapter {chapter_num}: {item.get_name()}\n\n")
                        text_parts.append(f"{text.strip()}\n\n")
                        
                        chapter_num += 1
            
            result['text'] = '\n'.join(text_parts)
            
        except Exception as e:
            result['error'] = str(e)
            result['text'] = f"Error processing EPUB: {str(e)}"
        
        return result
    
    def to_markdown(self, content: Dict[str, Any]) -> str:
        """Convert ebook content to markdown"""
        if isinstance(content, str):
            return content
        
        if content.get('text'):
            return content['text']
        
        # Fallback conversion
        markdown = "# Ebook\n\n"
        
        # Add metadata
        if content.get('metadata'):
            metadata = content['metadata']
            markdown += "## Book Information\n\n"
            for key, value in metadata.items():
                if value:
                    markdown += f"**{key.title()}:** {value}\n\n"
        
        # Add chapters
        if content.get('chapters'):
            markdown += "## Content\n\n"
            for chapter in content['chapters']:
                markdown += f"### Chapter {chapter['chapter_number']}: {chapter['title']}\n\n"
                markdown += f"{chapter['content']}\n\n"
                markdown += "---\n\n"
        
        return markdown
