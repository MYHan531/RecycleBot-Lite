#!/usr/bin/env python3
"""
Web Interface for NEA RAG System
Simple Flask web app for interacting with the RAG system
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from rag_system import NEARAGSystem, test_ollama_connection
except ImportError as e:
    print(f"Error importing RAG system: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

app = Flask(__name__)

# Global RAG system instance
rag_system = None

def initialize_rag_system():
    """Initialize the RAG system"""
    global rag_system
    try:
        if test_ollama_connection():
            rag_system = NEARAGSystem()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return False

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint for asking questions"""
    if rag_system is None:
        return jsonify({
            'error': 'RAG system not initialized. Please check Ollama installation.'
        }), 500
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # Get chat history from request
        chat_history = data.get('chat_history', [])
        
        # Ask question
        response = rag_system.ask_question(question, chat_history)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Check system status"""
    try:
        ollama_running = test_ollama_connection()
        rag_ready = rag_system is not None
        
        return jsonify({
            'ollama_running': ollama_running,
            'rag_system_ready': rag_ready,
            'status': 'ready' if (ollama_running and rag_ready) else 'not_ready'
        })
    except Exception as e:
        return jsonify({
            'ollama_running': False,
            'rag_system_ready': False,
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/similar', methods=['POST'])
def get_similar():
    """Get similar documents"""
    if rag_system is None:
        return jsonify({'error': 'RAG system not initialized'}), 500
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        k = data.get('k', 3)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        docs = rag_system.get_similar_documents(query, k)
        
        # Format documents for response
        formatted_docs = []
        for doc in docs:
            formatted_docs.append({
                'content': doc.page_content[:500] + '...' if len(doc.page_content) > 500 else doc.page_content,
                'source': doc.metadata.get('source', 'Unknown')
            })
        
        return jsonify({'documents': formatted_docs})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create templates directory and HTML template
def create_templates():
    """Create templates directory and HTML template"""
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEA Waste Management RAG System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .status.ready {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.not-ready {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .chat-container {
            border: 1px solid #ddd;
            border-radius: 5px;
            height: 400px;
            overflow-y: auto;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #fafafa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
            gap: 10px;
        }
        #question-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0056b3;
        }
        button:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
        .sources {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗑️ NEA Waste Management RAG System</h1>
        
        <div id="status" class="status not-ready">
            Checking system status...
        </div>
        
        <div class="chat-container" id="chat-container">
            <div class="message bot-message">
                Hello! I'm your NEA Waste Management assistant. Ask me anything about recycling, waste statistics, or waste management in Singapore.
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="question-input" placeholder="Ask a question about waste management..." disabled>
            <button id="ask-button" disabled>Ask</button>
        </div>
    </div>

    <script>
        let chatHistory = [];
        
        // Check system status
        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const statusDiv = document.getElementById('status');
                const input = document.getElementById('question-input');
                const button = document.getElementById('ask-button');
                
                if (data.status === 'ready') {
                    statusDiv.className = 'status ready';
                    statusDiv.textContent = '✅ System ready - Ask your questions!';
                    input.disabled = false;
                    button.disabled = false;
                } else {
                    statusDiv.className = 'status not-ready';
                    statusDiv.textContent = '❌ System not ready - Check Ollama installation';
                    input.disabled = true;
                    button.disabled = true;
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }
        
        // Add message to chat
        function addMessage(content, isUser = false, sources = []) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            
            let html = content;
            if (sources && sources.length > 0) {
                html += '<div class="sources">Sources: ' + sources.join(', ') + '</div>';
            }
            
            messageDiv.innerHTML = html;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // Ask question
        async function askQuestion() {
            const input = document.getElementById('question-input');
            const button = document.getElementById('ask-button');
            const question = input.value.trim();
            
            if (!question) return;
            
            // Disable input during processing
            input.disabled = true;
            button.disabled = true;
            
            // Add user message
            addMessage(question, true);
            input.value = '';
            
            // Add loading message
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading';
            loadingDiv.textContent = 'Thinking...';
            document.getElementById('chat-container').appendChild(loadingDiv);
            
            try {
                const response = await fetch('/api/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: question,
                        chat_history: chatHistory
                    })
                });
                
                const data = await response.json();
                
                // Remove loading message
                loadingDiv.remove();
                
                if (data.error) {
                    addMessage('Sorry, I encountered an error: ' + data.error);
                } else {
                    addMessage(data.answer, false, data.sources);
                    chatHistory.push([question, data.answer]);
                }
            } catch (error) {
                loadingDiv.remove();
                addMessage('Sorry, I encountered an error: ' + error.message);
            }
            
            // Re-enable input
            input.disabled = false;
            button.disabled = false;
            input.focus();
        }
        
        // Event listeners
        document.getElementById('ask-button').addEventListener('click', askQuestion);
        document.getElementById('question-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
        
        // Initial status check
        checkStatus();
        
        // Check status every 30 seconds
        setInterval(checkStatus, 30000);
    </script>
</body>
</html>'''
    
    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

def main():
    """Main function"""
    print("🌐 Starting NEA RAG System Web Interface...")
    
    # Create templates
    create_templates()
    
    # Initialize RAG system
    print("📚 Initializing RAG system...")
    if not initialize_rag_system():
        print("❌ Failed to initialize RAG system")
        print("Please ensure:")
        print("1. Ollama is installed and running")
        print("2. Llama3 model is pulled: ollama pull llama3")
        print("3. All dependencies are installed: pip install -r requirements.txt")
        return
    
    print("✅ RAG system initialized successfully")
    print("🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main() 