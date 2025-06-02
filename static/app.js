// TypeScript-style JavaScript for the Document Converter App

class DocumentConverter {
    constructor() {
        this.fileId = null;
        this.apiBaseUrl = '/api';
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File upload elements
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        
        // Drag and drop
        uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // File input
        fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        // Convert button
        document.getElementById('convert-btn').addEventListener('click', this.convertDocument.bind(this));
        
        // Split button
        document.getElementById('split-btn').addEventListener('click', this.splitText.bind(this));
        
        // Download buttons
        document.getElementById('download-original-btn').addEventListener('click', () => this.downloadFile('original'));
        document.getElementById('download-split-btn').addEventListener('click', () => this.downloadFile('split'));
        
        // Splitter type change
        document.getElementById('splitter-type').addEventListener('change', this.handleSplitterTypeChange.bind(this));
        
        // Show advanced options for recursive and character splitters
        this.handleSplitterTypeChange();
    }

    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('upload-area').classList.add('drag-over');
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('upload-area').classList.remove('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById('upload-area').classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    processFile(file) {
        this.displayFileInfo(file);
        this.uploadFile(file);
    }

    displayFileInfo(file) {
        const fileInfo = document.getElementById('file-info');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        
        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        fileInfo.classList.remove('hidden');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async uploadFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            this.showStatus('Uploading file...', 'info');
            
            const response = await fetch(`${this.apiBaseUrl}/upload`, {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.fileId = result.file_id;
                this.showStatus('File uploaded successfully!', 'success');
                document.getElementById('convert-btn').disabled = false;
            } else {
                this.showStatus(`Upload failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Upload error: ${error.message}`, 'error');
        }
    }

    async convertDocument() {
        if (!this.fileId) {
            this.showStatus('Please upload a file first', 'error');
            return;
        }

        try {
            const outputFormat = document.getElementById('output-format').value;
            
            this.showConvertLoading(true);
            
            const response = await fetch(`${this.apiBaseUrl}/convert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: this.fileId,
                    output_format: outputFormat
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showConvertResult(result);
                this.showStatus('Document converted successfully!', 'success');
                document.getElementById('split-btn').disabled = false;
            } else {
                this.showStatus(`Conversion failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Conversion error: ${error.message}`, 'error');
        } finally {
            this.showConvertLoading(false);
        }
    }

    async splitText() {
        if (!this.fileId) {
            this.showStatus('Please upload and convert a file first', 'error');
            return;
        }

        try {
            const splitterParams = this.getSplitterParams();
            const outputFormat = document.getElementById('output-format').value;
            
            this.showSplitLoading(true);
            
            const response = await fetch(`${this.apiBaseUrl}/split`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    file_id: this.fileId,
                    splitter_params: splitterParams,
                    output_format: outputFormat
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                this.showSplitResults(result);
                this.showStatus('Text split successfully!', 'success');
            } else {
                this.showStatus(`Splitting failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Splitting error: ${error.message}`, 'error');
        } finally {
            this.showSplitLoading(false);
        }
    }

    getSplitterParams() {
        const splitterType = document.getElementById('splitter-type').value;
        const chunkSize = parseInt(document.getElementById('chunk-size').value);
        const chunkOverlap = parseInt(document.getElementById('chunk-overlap').value);
        const keepSeparator = document.getElementById('keep-separator').checked;
        
        const params = {
            splitter_type: splitterType,
            chunk_size: chunkSize,
            chunk_overlap: chunkOverlap,
            keep_separator: keepSeparator
        };
        
        // Add separators if specified
        const separatorsInput = document.getElementById('separators').value.trim();
        if (separatorsInput && ['recursive', 'character'].includes(splitterType)) {
            params.separators = separatorsInput.split(',').map(s => s.trim().replace(/\\n/g, '\n'));
        }
        
        return params;
    }

    async downloadFile(fileType) {
        if (!this.fileId) {
            this.showStatus('No file to download', 'error');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/download/${this.fileId}/${fileType}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${fileType === 'split' ? 'split_' : ''}document.${document.getElementById('output-format').value}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                const result = await response.json();
                this.showStatus(`Download failed: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showStatus(`Download error: ${error.message}`, 'error');
        }
    }

    showConvertLoading(loading) {
        const convertBtn = document.getElementById('convert-btn');
        const convertText = document.getElementById('convert-text');
        const convertSpinner = document.getElementById('convert-spinner');
        
        convertBtn.disabled = loading;
        convertText.classList.toggle('hidden', loading);
        convertSpinner.classList.toggle('hidden', !loading);
    }

    showSplitLoading(loading) {
        const splitBtn = document.getElementById('split-btn');
        const splitText = document.getElementById('split-text');
        const splitSpinner = document.getElementById('split-spinner');
        
        splitBtn.disabled = loading;
        splitText.classList.toggle('hidden', loading);
        splitSpinner.classList.toggle('hidden', !loading);
    }

    showConvertResult(result) {
        const convertResult = document.getElementById('convert-result');
        const contentLength = document.getElementById('content-length');
        
        contentLength.textContent = result.content_length.toLocaleString();
        convertResult.classList.remove('hidden');
    }

    showSplitResults(result) {
        const splitResults = document.getElementById('split-results');
        const chunkCount = document.getElementById('chunk-count');
        const usedParams = document.getElementById('used-params');
        const previewContainer = document.getElementById('preview-container');
        
        chunkCount.textContent = result.chunk_count;
        usedParams.textContent = JSON.stringify(result.splitter_params, null, 0);
        
        // Show preview of first 3 chunks
        previewContainer.innerHTML = '';
        result.preview.forEach((chunk, index) => {
            const chunkDiv = document.createElement('div');
            chunkDiv.className = 'bg-gray-50 border rounded p-3';
            chunkDiv.innerHTML = `
                <div class="font-medium text-sm text-gray-600 mb-2">Chunk ${index + 1}</div>
                <div class="text-sm text-gray-800">${this.truncateText(chunk, 200)}</div>
            `;
            previewContainer.appendChild(chunkDiv);
        });
        
        splitResults.classList.remove('hidden');
    }

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    handleSplitterTypeChange() {
        const splitterType = document.getElementById('splitter-type').value;
        const separatorsInput = document.getElementById('separators-input');
        
        // Show separators input for recursive and character splitters
        if (['recursive', 'character'].includes(splitterType)) {
            separatorsInput.classList.remove('hidden');
        } else {
            separatorsInput.classList.add('hidden');
        }
    }

    showStatus(message, type) {
        const statusContainer = document.getElementById('status-messages');
        
        // Remove existing messages
        statusContainer.innerHTML = '';
        
        const alertClass = {
            'success': 'bg-green-50 border-green-200 text-green-800',
            'error': 'bg-red-50 border-red-200 text-red-800',
            'info': 'bg-blue-50 border-blue-200 text-blue-800'
        }[type] || 'bg-gray-50 border-gray-200 text-gray-800';
        
        const statusDiv = document.createElement('div');
        statusDiv.className = `${alertClass} border rounded-lg p-4 mb-4`;
        statusDiv.innerHTML = `
            <div class="flex">
                <div class="flex-1">${message}</div>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-current opacity-50 hover:opacity-100">&times;</button>
            </div>
        `;
        
        statusContainer.appendChild(statusDiv);
        
        // Auto-remove success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                if (statusDiv.parentElement) {
                    statusDiv.remove();
                }
            }, 5000);
        }
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new DocumentConverter();
});
