# Contributing to Pharmaceutical Compliance RAG System

We welcome contributions to improve the pharmaceutical compliance monitoring system! 

## 🤝 How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/your-username/pharma-rag-system.git
cd pharma-rag-system
```

### 2. Set Up Development Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your OpenRouter API key
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- Follow existing code style and structure
- Add tests for new functionality
- Update documentation as needed
- Test your changes locally

### 5. Test Your Changes
```bash
# Start the system
./start.sh

# Test upload functionality
curl -X POST -F 'file=@test_document.pdf' http://localhost:8001/v1/upload

# Test query functionality
curl -X POST http://localhost:8000/v1/pw_ai_answer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test query"}'
```

### 6. Submit Pull Request
- Push your changes to your fork
- Create a pull request with clear description
- Reference any related issues

## 🐛 Reporting Issues

- Use GitHub Issues for bug reports
- Include system information (OS, Python version)
- Provide steps to reproduce the problem
- Include relevant log output

## 💡 Feature Requests

- Use GitHub Issues with "enhancement" label
- Describe the pharmaceutical use case
- Explain expected behavior
- Consider implementation complexity

## 📝 Code Guidelines

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise
- Handle errors gracefully

## 🧪 Testing

- Test with various pharmaceutical document types
- Verify upload functionality with different file sizes
- Test query accuracy with domain-specific questions
- Check error handling with invalid inputs

## 📚 Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Update API documentation for new endpoints
- Include example usage in docstrings

Thank you for contributing to pharmaceutical compliance monitoring!