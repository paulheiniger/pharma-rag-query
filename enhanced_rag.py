#!/usr/bin/env python3
"""
Enhanced RAG Question Answerer with Similarity Filtering

This module extends Pathway's BaseRAGQuestionAnswerer to include
similarity threshold filtering to prevent hallucinations.
"""

import pathway as pw
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from typing import List, Dict, Any

class FilteredRAGQuestionAnswerer(BaseRAGQuestionAnswerer):
    """
    Enhanced RAG Question Answerer with similarity threshold filtering.
    
    Prevents hallucinations by filtering out documents that are not
    sufficiently similar to the query before sending to the LLM.
    """
    
    def __init__(self, similarity_threshold: float = 0.35, **kwargs):
        """
        Initialize the filtered RAG question answerer.
        
        Args:
            similarity_threshold: Minimum similarity score (0.0-1.0)
            **kwargs: Arguments passed to BaseRAGQuestionAnswerer
        """
        super().__init__(**kwargs)
        self.similarity_threshold = similarity_threshold
    
    @pw.udf
    def filter_documents_by_similarity(
        self, 
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Filter documents by similarity threshold.
        
        Args:
            documents: List of retrieved documents with distance scores
            
        Returns:
            Filtered list of relevant documents
        """
        filtered_docs = []
        
        for doc in documents:
            # Extract distance score
            distance = doc.get('dist', 1.0)
            
            # Convert to similarity (for cosine: similarity = 1 - distance)
            similarity = 1.0 - distance
            
            # Only keep documents above threshold
            if similarity >= self.similarity_threshold:
                # Add similarity score for debugging
                doc_copy = doc.copy()
                doc_copy['similarity'] = similarity
                filtered_docs.append(doc_copy)
        
        return filtered_docs

# Configuration for enhanced YAML
enhanced_config_template = """
# Enhanced RAG Configuration with Similarity Filtering
question_answerer: !pw.xpacks.llm.question_answering.BaseRAGQuestionAnswerer
  llm: $llm
  indexer: $document_store
  prompt_template: $prompt_template
  search_topk: 15                    # Get more results for filtering
  # Note: Custom filtering will be applied in post-processing
"""