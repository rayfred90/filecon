from typing import Dict, Any
from .base_processor import BaseProcessor

class TextProcessor(BaseProcessor):
    """Process plain text and code files"""
    
    def process(self, filepath: str) -> Dict[str, Any]:
        """Extract text from plain text files"""
        result = {
            'text': '',
            'metadata': {}
        }
        
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
            content = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                        used_encoding = encoding
                        break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                # Fallback: read as binary and decode with errors='ignore'
                with open(filepath, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    used_encoding = 'utf-8 (with errors ignored)'
            
            # Get file info
            file_extension = filepath.split('.')[-1].lower() if '.' in filepath else 'txt'
            
            result['metadata'] = {
                'file_type': file_extension,
                'encoding': used_encoding,
                'line_count': len(content.splitlines()),
                'character_count': len(content)
            }
            
            # Format content based on file type
            if file_extension in ['md', 'markdown']:
                result['text'] = content  # Markdown files are already formatted
            elif file_extension in ['json']:
                result['text'] = f"```json\n{content}\n```"
            elif file_extension in ['xml', 'html']:
                result['text'] = f"```xml\n{content}\n```"
            elif file_extension in ['yaml', 'yml']:
                result['text'] = f"```yaml\n{content}\n```"
            elif file_extension in ['sql']:
                result['text'] = f"```sql\n{content}\n```"
            elif file_extension in ['js', 'javascript']:
                result['text'] = f"```javascript\n{content}\n```"
            elif file_extension in ['ts', 'typescript']:
                result['text'] = f"```typescript\n{content}\n```"
            elif file_extension in ['py', 'python']:
                result['text'] = f"```python\n{content}\n```"
            elif file_extension in ['java']:
                result['text'] = f"```java\n{content}\n```"
            elif file_extension in ['cpp', 'c++', 'cc', 'cxx']:
                result['text'] = f"```cpp\n{content}\n```"
            elif file_extension in ['c']:
                result['text'] = f"```c\n{content}\n```"
            elif file_extension in ['go']:
                result['text'] = f"```go\n{content}\n```"
            elif file_extension in ['rust', 'rs']:
                result['text'] = f"```rust\n{content}\n```"
            elif file_extension in ['php']:
                result['text'] = f"```php\n{content}\n```"
            elif file_extension in ['css']:
                result['text'] = f"```css\n{content}\n```"
            elif file_extension in ['html', 'htm']:
                result['text'] = f"```html\n{content}\n```"
            else:
                # Plain text
                result['text'] = content
            
        except Exception as e:
            result['error'] = str(e)
            result['text'] = f"Error processing text file: {str(e)}"
        
        return result
    
    def to_markdown(self, content: Dict[str, Any]) -> str:
        """Convert text content to markdown"""
        if isinstance(content, str):
            return content
        
        markdown = ""
        
        # Add metadata
        if content.get('metadata'):
            metadata = content['metadata']
            markdown += f"# {metadata.get('file_type', 'Text').upper()} File\n\n"
            markdown += f"**Encoding:** {metadata.get('encoding', 'Unknown')}\n"
            markdown += f"**Lines:** {metadata.get('line_count', 0)}\n"
            markdown += f"**Characters:** {metadata.get('character_count', 0)}\n\n"
            markdown += "---\n\n"
        
        # Add content
        if content.get('text'):
            markdown += content['text']
        
        return markdown
