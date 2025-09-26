#!/usr/bin/env python3
"""
Example: Customizing Pathway RAG prompt in Python code
This shows how to override the default prompt programmatically
"""

import os
import pathway as pw
from pathway.xpacks.llm import prompts
from dotenv import load_dotenv

# Custom prompt function that replaces the default one
@pw.udf 
def custom_pharma_prompt(context: str, query: str, additional_rules: str = "") -> str:
    """
    Custom pharmaceutical compliance prompt - replaces the default Pathway prompt
    """
    
    prompt = (
        "🧬 PHARMACEUTICAL COMPLIANCE ANALYSIS:\n"
        "You are an expert pharmaceutical regulatory analyst specializing in Indian drug regulations.\n\n" 
        "Based on the regulatory documents and gazette notifications provided below, "
        "provide a detailed analysis of the query.\n\n"
        "IMPORTANT GUIDELINES:\n"
        "- Focus on CDSCO regulations, drug bans, approvals, and schedule classifications\n"
        "- Always cite specific gazette notification numbers when available\n"  
        "- Distinguish between banned, scheduled, controlled, and approved drugs\n"
        "- If no regulatory information is found, respond: 'No regulatory information available in provided sources'\n\n"
    )
    
    prompt += additional_rules + "\n\n"
    
    prompt += (
        "REGULATORY DOCUMENTS:\n"
        "=" * 50 + "\n"
        f"{context}\n"
        "=" * 50 + "\n\n"
        f"COMPLIANCE QUERY: {query}\n\n"
        "REGULATORY ANALYSIS:\n"
    )
    
    return prompt

# Example of how to use this in your app
def create_custom_rag_app():
    """
    Example showing how to create a RAG app with custom prompt
    """
    load_dotenv()
    
    # This would replace the YAML configuration approach
    from pathway.xpacks.llm import llms, embedders, splitters, parsers
    from pathway.xpacks.llm.document_store import DocumentStore
    from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
    
    # Data sources
    sources = pw.io.fs.read(
        path="./data", 
        format="binary",
        with_metadata=True
    )
    
    # Components (would need proper API keys)
    llm = llms.LiteLLMChat(
        model="anthropic/claude-sonnet-4",
        temperature=0.1,
        max_tokens=1000,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base=os.getenv("OPENROUTER_API_BASE"), 
        custom_llm_provider="openrouter"
    )
    
    embedder = embedders.SentenceTransformerEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Document store
    document_store = DocumentStore(
        docs=[sources],
        parser=parsers.UnstructuredParser(),
        splitter=splitters.TokenCountSplitter(max_tokens=600),
        retriever_factory=pw.stdlib.indexing.UsearchKnnFactory(
            reserved_space=1000,
            embedder=embedder,
            metric=pw.stdlib.indexing.USearchMetricKind.COS
        )
    )
    
    # RAG Question Answerer with CUSTOM PROMPT
    rag_app = BaseRAGQuestionAnswerer(
        llm=llm,
        indexer=document_store, 
        prompt_template=custom_pharma_prompt  # 🎯 This replaces the default prompt!
    )
    
    return rag_app

if __name__ == "__main__":
    print("📋 Custom Pathway Prompt Example")
    print("=" * 50)
    print("\nThis script shows two ways to customize the Pathway RAG prompt:")
    print("\n1. 📝 YAML Configuration (RECOMMENDED):")
    print("   - Add 'prompt_template' parameter to your YAML config")
    print("   - Use placeholders: {context} and {query}")
    print("   - Already implemented in your app_openrouter*.yaml files")
    
    print("\n2. 🐍 Python Code:")  
    print("   - Create custom UDF function like 'custom_pharma_prompt'")
    print("   - Pass it to BaseRAGQuestionAnswerer(prompt_template=custom_pharma_prompt)")
    print("   - Gives you full programmatic control")
    
    print("\n✅ Result:")
    print("   The default 'Please provide an answer based solely on the provided sources'")
    print("   will be replaced with your custom pharmaceutical compliance prompt!")
    
    print(f"\n🔍 Current custom prompt preview:")
    print("-" * 60)
    sample_prompt = custom_pharma_prompt("Sample documents...", "Is Drug X banned?")
    print(sample_prompt[:300] + "...")
    print("-" * 60)