# Contributing to Document Converter & Text Splitter

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub Issues tab to report bugs or request features
- Provide detailed descriptions including steps to reproduce
- Include system information (OS, Python version, browser)
- Attach relevant files or screenshots when applicable

### Suggesting Features
- Check existing issues to avoid duplicates
- Describe the feature's purpose and expected behavior
- Consider backward compatibility and performance implications
- Provide use cases and examples

### Code Contributions

#### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a feature branch: `git checkout -b feature/your-feature-name`

#### Code Standards
- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Comment complex logic

#### Frontend Standards
- Use semantic HTML5 elements
- Follow existing Tailwind CSS patterns
- Ensure responsive design principles
- Test across different browsers
- Keep JavaScript modular and well-documented

#### Testing
- Test all new features thoroughly
- Verify existing functionality isn't broken
- Test with various file types and sizes
- Include edge cases and error conditions
- Document any new testing procedures

#### Pull Request Process
1. Ensure your code follows the project's style guidelines
2. Update documentation for any new features
3. Add or update tests as needed
4. Update CHANGELOG.md with your changes
5. Submit a pull request with a clear description

## 📁 Project Structure

```
├── app.py                 # Main Flask application
├── text_splitter.py       # LangChain text splitting service
├── processors/            # Document processing modules
│   ├── base_processor.py  # Abstract base class
│   ├── pdf_processor.py   # PDF processing
│   ├── doc_processor.py   # Word documents
│   ├── excel_processor.py # Excel/CSV files
│   ├── ppt_processor.py   # PowerPoint
│   ├── ebook_processor.py # EPUB/MOBI
│   └── text_processor.py  # Text/code files
├── static/                # Frontend files
│   ├── index.html         # Main web interface
│   └── app.js            # JavaScript logic
├── uploads/              # Temporary file storage
├── outputs/              # Processed file storage
└── requirements.txt      # Python dependencies
```

## 🔧 Development Guidelines

### Adding New Document Processors
1. Create a new processor class in `processors/`
2. Inherit from `BaseProcessor`
3. Implement required methods: `process()`, `to_markdown()`, `validate()`
4. Add file extension mapping in `app.py`
5. Update documentation and tests

### Adding New Text Splitters
1. Check LangChain documentation for available splitters
2. Add splitter to `text_splitter.py` in `TextSplitterService`
3. Update frontend options in `index.html`
4. Add configuration parameters as needed
5. Test with various text types

### API Changes
- Maintain backward compatibility when possible
- Version new API endpoints if breaking changes are necessary
- Update API documentation in README.md
- Test all endpoints thoroughly

## 🐛 Debugging

### Common Issues
- **Import Errors**: Check virtual environment activation
- **File Processing Errors**: Verify file format support
- **Memory Issues**: Monitor file sizes and chunk parameters
- **Frontend Issues**: Check browser console for JavaScript errors

### Development Server
```bash
export FLASK_ENV=development
python app.py
```

### Logging
- Enable debug mode for detailed error messages
- Check server logs for API request/response information
- Use browser developer tools for frontend debugging

## 📚 Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Libraries Used
- **pdfplumber**: PDF text extraction
- **python-docx**: Word document processing
- **pandas**: Data manipulation for Excel/CSV
- **openpyxl**: Excel file handling
- **python-pptx**: PowerPoint processing
- **ebooklib**: EPUB processing

## 🎯 Priority Areas for Contribution

1. **Additional File Format Support**
   - RTF documents
   - OpenDocument formats (ODT, ODS, ODP)
   - Additional eBook formats
   - Archive files (ZIP, RAR)

2. **Enhanced Text Processing**
   - OCR support for scanned documents
   - Table extraction improvements
   - Image and chart handling
   - Metadata preservation

3. **User Interface Improvements**
   - Batch file processing
   - Progress bars for large files
   - File preview capabilities
   - Advanced configuration options

4. **Performance Optimization**
   - Streaming for large files
   - Background processing
   - Caching mechanisms
   - Memory usage optimization

5. **Integration Features**
   - Cloud storage support (S3, Google Drive, Dropbox)
   - API authentication
   - Webhook support
   - Database integration

## 📝 Commit Message Guidelines

Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example: `feat: add support for RTF document processing`

## 🏷️ Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Community

- Be respectful and inclusive
- Help newcomers get started
- Share knowledge and best practices
- Provide constructive feedback

Thank you for contributing to making document processing more accessible and efficient! 🚀
