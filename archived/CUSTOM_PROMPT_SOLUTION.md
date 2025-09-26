# 🧬 Custom Pathway RAG Prompt Solution

## Problem
The user noticed **"Please provide an answer based solely on the provided sources"** appearing in the Pathway LLM logs and wanted to customize this default prompt for their pharmaceutical compliance use case.

## Root Cause
This text comes from Pathway's default prompt templates in the LLM xpack:
- `prompts.prompt_qa()` - Default RAG prompt function
- `prompts.prompt_short_qa()` - Short answer prompt
- `prompts.prompt_citing_qa()` - Citation-focused prompt

When using `BaseRAGQuestionAnswerer` without specifying a custom `prompt_template`, it uses the default `prompts.prompt_qa` which includes this hardcoded text.

## Solution ✅

### Method 1: YAML Configuration (RECOMMENDED)
Add a custom `prompt_template` to your YAML configuration files:

```yaml
# Custom prompt template for pharmaceutical compliance
$prompt_template: |
  You are a pharmaceutical compliance expert. Analyze the provided regulatory documents and answer questions about drug bans, approvals, and regulatory status in India.
  
  Based on the provided sources below, provide a comprehensive answer to the question.
  If the information cannot be found in the sources, respond with "No regulatory information found."
  
  When referencing specific regulations, always cite the source document and gazette notification number if available.
  
  Context Documents:
  {context}
  
  Question: {query}
  
  Answer:

# Enhanced question answerer 
question_answerer: !pw.xpacks.llm.question_answering.BaseRAGQuestionAnswerer
  llm: $llm
  indexer: $document_store
  prompt_template: $prompt_template  # 🎯 This replaces the default!
```

### Method 2: Python Code
```python
import pathway as pw

@pw.udf 
def custom_pharma_prompt(context: str, query: str, additional_rules: str = "") -> str:
    prompt = (
        "🧬 PHARMACEUTICAL COMPLIANCE ANALYSIS:\n"
        "You are an expert pharmaceutical regulatory analyst...\n"
        # ... custom prompt logic
    )
    return prompt

# Use in BaseRAGQuestionAnswerer
rag_app = BaseRAGQuestionAnswerer(
    llm=llm,
    indexer=document_store, 
    prompt_template=custom_pharma_prompt  # Custom function
)
```

## Files Modified ✅

1. **`app_openrouter_enhanced.yaml`** - Added custom pharmaceutical compliance prompt
2. **`app_openrouter.yaml`** - Added custom pharmaceutical compliance prompt
3. **`test_prompt_replacement.py`** - Verification script
4. **`example_custom_prompt.py`** - Example showing both methods

## Key Requirements

- **Placeholders**: Must use `{context}` and `{query}` in your custom template
- **Virtual Environment**: Always work within `venv/` for proper dependencies
- **Activation**: `source venv/bin/activate` before running any Python scripts

## Testing ✅

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Verify configuration
python test_prompt_replacement.py

# 3. Start server
python app_openrouter_enhanced.py

# 4. Test live (in another terminal)
source venv/bin/activate
python test_prompt_replacement.py --test-live
```

## Result ✅

**Before**: 
```
"Please provide an answer based solely on the provided sources. Keep your answer concise..."
```

**After**: 
```
"You are a pharmaceutical compliance expert. Analyze the provided regulatory documents..."
```

## Benefits

1. **🎯 Domain-Specific**: Tailored for pharmaceutical compliance use case
2. **📋 Better Context**: Instructs LLM about Indian drug regulations specifically  
3. **🔗 Citations**: Encourages citing gazette notifications and source documents
4. **⚠️ Custom Errors**: Uses "No regulatory information found" instead of generic messages
5. **🧬 Professional**: More professional tone for pharmaceutical regulatory queries

## Future Enhancements

- Add specific instruction for FDC (Fixed Dose Combination) handling
- Include templates for different query types (ban status, approval status, scheduling)
- Add validation for gazette notification format requirements
- Implement multi-language support for regulatory documents

---

**Status**: ✅ **SOLVED** - Default Pathway prompt successfully replaced with custom pharmaceutical compliance prompt.