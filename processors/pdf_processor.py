import pdfplumber
from typing import Dict, Any, List
from .base_processor import BaseProcessor

class PDFProcessor(BaseProcessor):
    """Process PDF files including scanned PDFs"""
    
    def process(self, filepath: str) -> Dict[str, Any]:
        """Extract text and tables from PDF"""
        result = {
            'text': '',
            'tables': [],
            'pages': [],
            'metadata': {}
        }
        
        try:
            with pdfplumber.open(filepath) as pdf:
                # Extract metadata
                if pdf.metadata:
                    result['metadata'] = {
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'subject': pdf.metadata.get('Subject', ''),
                        'creator': pdf.metadata.get('Creator', ''),
                        'pages': len(pdf.pages)
                    }
                
                full_text = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_data = {
                        'page_number': page_num,
                        'text': '',
                        'tables': []
                    }
                    
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        page_text = page_text.strip()
                        page_data['text'] = page_text
                        full_text.append(f"--- Page {page_num} ---\n{page_text}")
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table_idx, table in enumerate(tables):
                            if table:
                                table_data = {
                                    'page': page_num,
                                    'table_index': table_idx,
                                    'data': table
                                }
                                page_data['tables'].append(table_data)
                                result['tables'].append(table_data)
                                
                                # Add table as markdown to text
                                table_md = self._table_to_markdown(table)
                                full_text.append(f"\n--- Table {table_idx + 1} (Page {page_num}) ---\n{table_md}")
                    
                    result['pages'].append(page_data)
                
                result['text'] = '\n\n'.join(full_text)
                
        except Exception as e:
            result['error'] = str(e)
            result['text'] = f"Error processing PDF: {str(e)}"
        
        return result
    
    def _table_to_markdown(self, table: List[List[str]]) -> str:
        """Convert table data to markdown format"""
        if not table or not table[0]:
            return ""
        
        markdown = ""
        
        # Header row
        if table[0]:
            headers = [str(cell) if cell else "" for cell in table[0]]
            markdown += "| " + " | ".join(headers) + " |\n"
            markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        # Data rows
        for row in table[1:]:
            if row:
                cells = [str(cell) if cell else "" for cell in row]
                # Pad row to match header length
                while len(cells) < len(headers):
                    cells.append("")
                markdown += "| " + " | ".join(cells) + " |\n"
        
        return markdown
    
    def to_markdown(self, content: Dict[str, Any]) -> str:
        """Convert PDF content to markdown"""
        if isinstance(content, str):
            return content
        
        markdown = ""
        
        # Add metadata
        if content.get('metadata'):
            metadata = content['metadata']
            markdown += "# Document Information\n\n"
            for key, value in metadata.items():
                if value:
                    markdown += f"**{key.title()}:** {value}\n\n"
        
        # Add main text content
        if content.get('text'):
            markdown += "# Content\n\n"
            markdown += content['text']
        
        return markdown
