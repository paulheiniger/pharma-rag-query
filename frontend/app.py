from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import os
import requests
import json
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pharma-safe-secret-key-2024'
app.config['UPLOAD_FOLDER'] = '../data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
upload_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def call_search_api(query):
    """
    Real API function to call the external search API
    API Endpoint: http://82.112.235.26:8001/v1/pw_ai_answer
    Format: {"prompt": "query text"}
    """
    api_url = "http://82.112.235.26:8001/v1/pw_ai_answer"
    
    # Prepare the request data with the exact format from curl
    request_data = {
        "prompt": query
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"\n🚀 === BACKEND: Flask → External API ===")
    print(f"🎯 External API URL: {api_url}")
    print(f"🔑 Key: 'prompt'")
    print(f"📝 Value: '{query}'")
    print(f"📡 Making external API call...")
    
    try:
        # Make the API call with 2-minute timeout
        print("📡 Sending request...")
        print(f"🌐 URL: {api_url}")
        print(f"📦 Headers: {headers}")
        print(f"📝 JSON Body: {json.dumps(request_data, indent=2)}")
        
        response = requests.post(
            api_url,
            json=request_data,
            headers=headers,
            timeout=120  # 2 minutes timeout
        )
        
        print(f"✅ Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ API Response: {json.dumps(response_data, indent=2)}")
            return {
                "status": "success",
                "prompt": query,
                "api_response": response_data,
                "api_url": api_url,
                "processing_time": "API call completed"
            }
        else:
            print(f"❌ API Error: Status {response.status_code}")
            print(f"❌ Error Response: {response.text}")
            return {
                "status": "error",
                "error": f"API returned status {response.status_code}",
                "prompt": query,
                "api_url": api_url
            }
            
    except requests.exceptions.Timeout:
        print("⏰ API call timed out after 2 minutes")
        return {
            "status": "error",
            "error": "API request timed out after 2 minutes",
            "prompt": query,
            "api_url": api_url
        }
    except requests.exceptions.ConnectionError as e:
        print(f"🌐 Connection Error: {str(e)}")
        return {
            "status": "error",
            "error": f"Connection error: {str(e)}",
            "prompt": query,
            "api_url": api_url
        }
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "prompt": query,
            "api_url": api_url
        }

def call_document_analysis_api(file_paths):
    """
    Dummy function for document analysis - REPLACE THIS WITH YOUR UPLOAD API
    When you get the real upload API, just replace this function
    """
    # Simulate processing delay
    time.sleep(2)
    
    print(f"\n📄 === DUMMY UPLOAD API (Replace with real API) ===")
    print(f"📁 Files to process: {[os.path.basename(path) for path in file_paths]}")
    print(f"📊 Processing {len(file_paths)} documents...")
    
    # Dummy response structure
    response = {
        "status": "success",
        "documents_processed": len(file_paths),
        "files": [os.path.basename(path) for path in file_paths],
        "safety_analysis": "Document analysis completed. No banned substances detected.",
        "regulatory_status": "All mentioned medications comply with FDA regulations.",
        "risk_assessment": "Low to moderate risk profile identified.",
        "recommendations": "Follow standard pharmaceutical protocols.",
        "processing_time": "2.3 seconds"
    }
    
    print(f"✅ Dummy Response: {json.dumps(response, indent=2)}")
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
        return redirect(url_for('banportal'))
    
    try:
        # Call API for search queries
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

@app.route('/api/upload-files', methods=['POST'])
def api_upload_files():
    """API endpoint for file upload with status notifications"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No files provided'
            }), 400
        
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({
                'success': False,
                'message': 'No files selected'
            }), 400
        
        uploaded_files = []
        uploaded_file_names = []
        
        # Process each file
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                # Option 1: Direct file save (current implementation)
                file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(file_path)
                uploaded_files.append(file_path)
                uploaded_file_names.append(filename)
                print(f"📁 File uploaded successfully: {filename} -> {file_path}")
                
                # Option 2: External API call (if you want to use an API instead)
                # upload_api_url = "http://82.112.235.26:8001/v1/pw_upload_document"
                # files_data = {'file': (filename, file.read(), 'application/pdf')}
                # response = requests.post(upload_api_url, files=files_data, timeout=60)
                # if response.status_code == 200:
                #     uploaded_files.append(filename)
                #     uploaded_file_names.append(filename)
                #     print(f"📁 File uploaded via API: {filename}")
                # else:
                #     print(f"❌ API upload failed for {filename}: {response.status_code}")
        
        if not uploaded_files:
            return jsonify({
                'success': False,
                'message': 'No valid PDF files uploaded'
            }), 400
        
        # Return success response
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(uploaded_files)} file(s)',
            'files': uploaded_file_names,
            'count': len(uploaded_files),
            'upload_path': os.path.abspath(app.config['UPLOAD_FOLDER'])
        })
        
    except Exception as e:
        print(f"❌ Upload Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Upload failed: {str(e)}'
        }), 500

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search queries"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
        
        query = data['prompt']
        print(f"📥 Received prompt from frontend: {query}")
        
        response = call_search_api(query)
        
        print(f"📤 Sending response to frontend: {json.dumps(response, indent=2)}")
        return jsonify(response)
    except Exception as e:
        print(f"❌ Backend API Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-documents', methods=['POST'])
def api_analyze_documents():
    """API endpoint for document analysis - REPLACE WITH YOUR REAL API"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        print(f"📄 === UPLOAD API CALL ===")
        print(f"📁 Files received: {len(files)}")
        
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
        
        # Call dummy upload API (REPLACE THIS)
        response = call_document_analysis_api(file_paths)
        
        # Clean up files
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        return jsonify(response)
    except Exception as e:
        print(f"❌ Upload API Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/list-documents', methods=['POST', 'OPTIONS'])
def list_documents():
    """Fetch list of documents from the RAG database"""
    
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        print(f"\n[DOCUMENTS] === FETCHING DOCUMENT LIST ===")
        print(f"[DOCUMENTS] Request method: {request.method}")
        print(f"[DOCUMENTS] Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Make API call to get document list
        api_url = "http://api.lehana.in:8001/v1/pw_list_documents"
        
        print(f"[DOCUMENTS] Calling API: {api_url}")
        
        response = requests.post(
            api_url,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"[DOCUMENTS] API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            documents = response.json()
            print(f"[DOCUMENTS] Retrieved {len(documents)} documents")
            
            # Add CORS headers to response
            resp = jsonify(documents)
            resp.headers.add('Access-Control-Allow-Origin', '*')
            resp.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            resp.headers.add('Access-Control-Allow-Methods', 'POST')
            
            return resp
        else:
            print(f"[DOCUMENTS] API Error: {response.status_code}")
            error_response = jsonify({
                'error': f'Document API returned status {response.status_code}',
                'status': 'error'
            })
            error_response.headers.add('Access-Control-Allow-Origin', '*')
            return error_response, response.status_code
            
    except requests.exceptions.RequestException as e:
        print(f"[DOCUMENTS] Connection Error: {str(e)}")
        error_response = jsonify({
            'error': f'Failed to connect to document API: {str(e)}',
            'status': 'connection_error'
        })
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 503
        
    except Exception as e:
        print(f"[DOCUMENTS] Unexpected Error: {str(e)}")
        error_response = jsonify({
            'error': f'Unexpected error: {str(e)}',
            'status': 'error'
        })
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

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
    print("🚀 Starting PharmaSafe Server...")
    print("🌐 Access the application at: http://localhost:8002/banportal")
    print("📡 API endpoints available at: /api/search and /api/analyze-documents")
    print("❤️ Health check at: /health")
    print("\n🔧 To integrate with real APIs:")
    print("   1. The search API is already integrated with: http://82.112.235.26:8001/v1/pw_ai_answer")
    print("   2. Replace call_document_analysis_api() function with your real upload API")
    print("   3. Update /api/analyze-documents endpoint when you get the real upload API")
    print("\n🎯 Starting development server on port 8002...")
    
    app.run(debug=True, host='0.0.0.0', port=8002)
