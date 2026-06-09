import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generatedHTML, setGeneratedHTML] = useState('');
  const [style, setStyle] = useState('modern');
  const [error, setError] = useState('');
  const [documentInfo, setDocumentInfo] = useState(null);
  const [downloadFormat, setDownloadFormat] = useState('html'); // 'html' or 'zip'

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
      setError('');
    },
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  });

  const convertDocument = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('style', style);

    try {
      const response = await axios.post('http://localhost:8000/convert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setGeneratedHTML(response.data.html);
        setDocumentInfo({
          length: response.data.document_length,
          tokens: response.data.tokens_used,
          filename: file.name.split('.')[0]
        });
      }
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'Conversion failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Download as HTML file
  const downloadAsHTML = () => {
    const blob = new Blob([generatedHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${documentInfo?.filename || 'website'}.html`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Download as ZIP file
  const downloadAsZip = async () => {
    try {
      setLoading(true);
      const response = await axios.post(
        'http://localhost:8000/download-as-zip',
        {
          html_content: generatedHTML,
          filename: documentInfo?.filename || 'website'
        },
        {
          responseType: 'blob' // Important for file download
        }
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${documentInfo?.filename || 'website'}_website.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (err) {
      console.error('Download error:', err);
      setError('Failed to create ZIP file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Combined download function
  const handleDownload = () => {
    if (downloadFormat === 'html') {
      downloadAsHTML();
    } else {
      downloadAsZip();
    }
  };

  const clearFile = () => {
    setFile(null);
    setGeneratedHTML('');
    setDocumentInfo(null);
    setError('');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📄 Document to Website Converter</h1>
        <p>Upload any document and watch AI transform it into a beautiful website</p>
      </header>

      <div className="container">
        {!generatedHTML ? (
          <div className="upload-section">
            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
              <input {...getInputProps()} />
              <div className="dropzone-content">
                {file ? (
                  <>
                    <span className="file-icon">📎</span>
                    <p className="file-name">{file.name}</p>
                    <small className="file-size">{(file.size / 1024).toFixed(2)} KB</small>
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        clearFile();
                      }} 
                      className="remove-file"
                    >
                      ✕ Remove
                    </button>
                  </>
                ) : (
                  <>
                    <span className="upload-icon">📁</span>
                    <p>Drag & drop or click to upload</p>
                    <small>Supports PDF, DOCX, TXT (Max 10MB)</small>
                  </>
                )}
              </div>
            </div>

            {file && (
              <div className="controls">
                <div className="style-selector">
                  <label>🎨 Design Style:</label>
                  <select value={style} onChange={(e) => setStyle(e.target.value)}>
                    <option value="modern">Modern (Glassmorphism)</option>
                    <option value="minimal">Minimal & Clean</option>
                    <option value="corporate">Corporate Professional</option>
                    <option value="playful">Playful & Colorful</option>
                    <option value="dark">Dark Theme / Neon</option>
                  </select>
                </div>

                <button 
                  onClick={convertDocument} 
                  disabled={loading}
                  className="convert-btn"
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      AI is building your website...
                    </>
                  ) : (
                    '🚀 Convert to Website'
                  )}
                </button>
              </div>
            )}

            {error && <div className="error">{error}</div>}
          </div>
        ) : (
          <div className="result-section">
            <div className="result-header">
              <div>
                <h2>✨ Your Website is Ready!</h2>
                {documentInfo && (
                  <p className="stats">
                    📝 {documentInfo.length} characters processed
                    {documentInfo.tokens && ` • 🎯 ${documentInfo.tokens} tokens used`}
                  </p>
                )}
              </div>
              <div className="result-actions">
                <div className="download-options">
                  <label>Download as:</label>
                  <select 
                    value={downloadFormat} 
                    onChange={(e) => setDownloadFormat(e.target.value)}
                    className="format-select"
                  >
                    <option value="html">HTML File</option>
                    <option value="zip">ZIP Archive (with README)</option>
                  </select>
                </div>
                <button onClick={handleDownload} className="download-btn" disabled={loading}>
                  💾 Download {downloadFormat === 'zip' ? 'ZIP' : 'HTML'}
                </button>
                <button onClick={clearFile} className="new-btn">
                  📄 Convert Another Document
                </button>
              </div>
            </div>
            
            <div className="preview-container">
              <div className="preview-toolbar">
                <span>🔍 Live Preview</span>
                <button onClick={() => window.open('data:text/html,' + encodeURIComponent(generatedHTML), '_blank')}>
                  🖥️ Open in New Tab
                </button>
              </div>
              <iframe 
                srcDoc={generatedHTML}
                title="Generated Website"
                className="preview-frame"
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
              />
            </div>
          </div>
        )}
      </div>

      <footer className="footer">
        <p>Powered by Mistral AI • Free for portfolio use</p>
      </footer>
    </div>
  );
}

export default App;