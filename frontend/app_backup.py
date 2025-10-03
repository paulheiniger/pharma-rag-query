from flask import Flask, render_template    print(f"\n🚀 === BACKEND: Flask → External API ===")
    print(f"🎯 External API URL: {api_url}")
    print(f"🔑 Key: 'prompt'")
    print(f"📝 Value: '{query}'")
    print(f"📡 Making external API call...")ng, request, redirect, url_for, jsonify
import os
import requests
import json
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pharma-safe-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dummy API functions (replace these with actual API calls)
def call_search_api(query):
    """
    Real API function to call the external search API
    API Endpoint: http://82.112.235.26:8000/v1/pw_ai_answer
    Format: {"prompt": "query text"}
    """
    api_url = "http://82.112.235.26:8000/v1/pw_ai_answer"
    
    # Prepare the request data with the exact format from curl
    request_data = {
        "prompt": query
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"\n� === BACKEND: Flask → External API ===")
    print(f"� External API URL: {API_URL}")
    print(f"� Key: 'prompt'")
    print(f"📝 Value: '{query}'")
    print(f"� Making external API call...")
    
    try:
        # Make the API call with 2-minute timeout
        print("📡 Sending request...")
        response = requests.post(
            api_url, 
            json=request_data,
            headers=headers,
            timeout=120  # 2 minutes timeout
        )
        
        print(f"\n📊 === API RESPONSE DETAILS ===")
        print(f"🎯 Status Code: {response.status_code}")
        print(f"⏱️ Response Time: {response.elapsed.total_seconds():.2f} seconds")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        response.raise_for_status()  # Raise exception for bad status codes
        
        try:
            api_response = response.json()
            print(f"✅ Response JSON: {json.dumps(api_response, indent=2)}")
        except json.JSONDecodeError:
            print(f"📄 Response Text: {response.text}")
            api_response = {"raw_response": response.text}
        
        print("=" * 40)
        
        return {
            "status": "success",
            "query": query,
            "api_response": api_response,
            "processing_time": f"{response.elapsed.total_seconds():.2f} seconds",
            "status_code": response.status_code
        }
        
    except requests.exceptions.Timeout:
        error_msg = "API request timed out after 2 minutes"
        print(f"\n⏰ TIMEOUT ERROR: {error_msg}")
        return {
            "status": "error",
            "error": error_msg,
            "query": query,
            "api_url": api_url
        }
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        print(f"\n❌ REQUEST ERROR: {error_msg}")
        return {
            "status": "error", 
            "error": error_msg,
            "query": query,
            "api_url": api_url
        }
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"\n🔥 UNEXPECTED ERROR: {error_msg}")
        return {
            "status": "error",
            "error": error_msg,
            "query": query,
            "api_url": api_url
        }

def call_document_analysis_api(file_paths):
    """
    Dummy function for document upload analysis
    
    TODO: Replace with real upload API when available
    EASY CHANGE: Just replace the entire function body below with your real API call
    
    Example for future real API:
    # api_url = "http://your-api-server.com/upload-endpoint"
    # files = [('files', open(path, 'rb')) for path in file_paths]
    # response = requests.post(api_url, files=files, timeout=120)
    # return response.json()
    """
    print(f"[UPLOAD API] Processing {len(file_paths)} files")
    print(f"[UPLOAD API] Files: {[os.path.basename(path) for path in file_paths]}")
    
    # Simulate processing delay (remove this when using real API)
    time.sleep(3)
    
    # Dummy response structure - customize this based on your future API
    response = {
        "status": "success",
        "documents_processed": len(file_paths),
        "files": [os.path.basename(path) for path in file_paths],
        "analysis_result": "Document analysis completed successfully.",
        "banned_substances": [],
        "safety_score": 85,
        "regulatory_compliance": "Documents appear to comply with FDA regulations.",
        "risk_assessment": "Low risk profile identified in uploaded documents.",
        "recommendations": [
            "Continue monitoring for regulatory updates",
            "Regular compliance audits recommended",
            "Follow standard pharmaceutical protocols"
        ],
        "processing_time": "3.2 seconds",
        "api_version": "dummy_v1.0"
    }
    
    print(f"[UPLOAD API] Dummy response: {json.dumps(response, indent=2)}")
    return response

# Load HTML templates
def load_template(template_name):
    """Load HTML template from file"""
    try:
        with open(template_name, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Template {template_name} not found"

@app.route('/')
def root():
    """Root route redirects to banportal"""
    return redirect(url_for('banportal'))

@app.route('/banportal')
def banportal():
    """Main page route for banned pharma portal"""
    try:
        template = load_template('index.html')
        return render_template_string(template)
    except Exception as e:
        return f"Error loading index page: {str(e)}", 500

@app.route('/analyze')
def analyze():
    """Analysis results page route"""
    query = request.args.get('query', '')
    analysis_type = request.args.get('type', 'search')
    
    if not query and analysis_type == 'search':
        return redirect(url_for('index'))
    
    try:
        # Call dummy API for search queries
        if analysis_type == 'search':
            api_response = call_search_api(query)
        
        template = load_template('result.html')
        return render_template_string(template)
    except Exception as e:
        return f"Error loading results page: {str(e)}", 500

@app.route('/esportal')
def esportal():
    """Redirect esportal to banportal"""
    return redirect(url_for('banportal'))

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and analysis"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(file_path)
        
        if not uploaded_files:
            return jsonify({'error': 'No valid PDF files uploaded'}), 400
        
        # Call dummy document analysis API
        api_response = call_document_analysis_api(uploaded_files)
        
        # Clean up uploaded files (optional - remove if you want to keep them)
        for file_path in uploaded_files:
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        # Redirect to results page with upload type
        query_param = f"Document Analysis: {len(uploaded_files)} files processed"
        return redirect(url_for('analyze', query=query_param, type='upload'))
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search queries"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        query = data['query']
        response = call_search_api(query)
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-documents', methods=['POST'])
def api_analyze_documents():
    """API endpoint for document analysis"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        # Process files similar to upload route
        file_paths = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
        
        if not file_paths:
            return jsonify({'error': 'No valid files processed'}), 400
        
        response = call_document_analysis_api(file_paths)
        
        # Clean up files
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PharmaSafe API',
        'version': '1.0.0',
        'timestamp': time.time()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(" Starting PharmaSafe Server...")
    print(" Access the application at: http://localhost:3000/banportal")
    print(" API endpoints available at: /api/search and /api/analyze-documents")
    print(" Health check at: /health")
    print("\n To integrate with real APIs:")
    print("   1. Replace call_search_api() function with your search API")
    print("   2. Replace call_document_analysis_api() function with your RAG API")
    print("   3. Update API endpoints in the functions above")
    print("\n Starting development server...")
    
    app.run(debug=True, host='0.0.0.0', port=3000)
