#!/usr/bin/env python3
"""
Sample Python file for testing the document converter and text splitter.
This file contains multiple functions and classes to test code splitting.
"""

import os
import sys
from typing import List, Dict, Optional

class DocumentProcessor:
    """A sample class for processing documents."""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.processed_count = 0
    
    def validate_paths(self) -> bool:
        """Validate that input and output paths exist."""
        if not os.path.exists(self.input_path):
            print(f"Input path {self.input_path} does not exist")
            return False
        
        output_dir = os.path.dirname(self.output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        return True
    
    def process_file(self, filename: str) -> Dict[str, str]:
        """Process a single file and return results."""
        filepath = os.path.join(self.input_path, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple processing: count words and lines
        word_count = len(content.split())
        line_count = len(content.splitlines())
        
        result = {
            'filename': filename,
            'word_count': str(word_count),
            'line_count': str(line_count),
            'content_preview': content[:200] + '...' if len(content) > 200 else content
        }
        
        self.processed_count += 1
        return result

def get_file_list(directory: str, extensions: List[str]) -> List[str]:
    """Get list of files with specified extensions from directory."""
    files = []
    for filename in os.listdir(directory):
        if any(filename.endswith(ext) for ext in extensions):
            files.append(filename)
    return sorted(files)

def main():
    """Main function to run the document processor."""
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_dir> <output_dir>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    processor = DocumentProcessor(input_dir, output_dir)
    
    if not processor.validate_paths():
        sys.exit(1)
    
    # Process text files
    text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css']
    files = get_file_list(input_dir, text_extensions)
    
    print(f"Found {len(files)} files to process")
    
    for filename in files:
        try:
            result = processor.process_file(filename)
            print(f"Processed {result['filename']}: {result['word_count']} words, {result['line_count']} lines")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"Total files processed: {processor.processed_count}")

if __name__ == "__main__":
    main()
