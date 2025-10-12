#!/usr/bin/env python3
"""
Similarity Threshold Filter for Pathway RAG System

This module adds similarity threshold filtering to prevent hallucinations
by filtering out documents that are not sufficiently similar to the query.

Key Features:
- Cosine similarity threshold filtering
- Customizable similarity cutoff values
- Works with existing UsearchKnnFactory setup
- Prevents irrelevant document retrieval
"""

import pathway as pw
from typing import List, Tuple, Dict, Any

@pw.udf
def filter_by_similarity_threshold(
    results: List[Dict[str, Any]], 
    similarity_threshold: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Filter retrieval results by similarity threshold to prevent hallucinations.
    
    Args:
        results: List of retrieval results with 'dist' (distance) scores
        similarity_threshold: Minimum similarity score (0.0 to 1.0)
                            Lower values = more strict filtering
                            
    Note: 
        - USearch returns 'dist' (distance) where lower = more similar
        - For cosine similarity: similarity = 1 - distance
        - We filter OUT results where similarity < threshold
    
    Returns:
        Filtered list of results above the similarity threshold
    """
    filtered_results = []
    
    for result in results:
        # Convert distance to similarity score
        # For cosine distance: similarity = 1 - distance
        distance = result.get('dist', 1.0)
        similarity = 1.0 - distance
        
        # Only keep results above threshold
        if similarity >= similarity_threshold:
            # Add similarity score to result for debugging
            result_with_similarity = result.copy()
            result_with_similarity['similarity'] = similarity
            filtered_results.append(result_with_similarity)
    
    return filtered_results

@pw.udf 
def filter_retrieve_response(
    response_data: Dict[str, Any],
    similarity_threshold: float = 0.3
) -> Dict[str, Any]:
    """
    Filter the retrieve API response to remove low-similarity results.
    
    Args:
        response_data: The JSON response from retrieve API
        similarity_threshold: Minimum similarity threshold
        
    Returns:
        Filtered response with only high-similarity results
    """
    # Handle both direct list and nested response formats
    if isinstance(response_data, list):
        # Direct list of results
        results = response_data
    elif isinstance(response_data, dict) and 'results' in response_data:
        # Nested format with 'results' key
        results = response_data['results']
    else:
        # Unknown format, return as-is
        return response_data
    
    # Apply similarity filtering
    filtered_results = filter_by_similarity_threshold(results, similarity_threshold)
    
    # Return in same format as input
    if isinstance(response_data, list):
        return filtered_results
    else:
        filtered_response = response_data.copy()
        filtered_response['results'] = filtered_results
        return filtered_response

# Configuration presets for different use cases
SIMILARITY_THRESHOLDS = {
    'strict': 0.5,      # Very strict - only highly relevant results
    'moderate': 0.3,    # Balanced - good relevance filtering
    'lenient': 0.2,     # Lenient - minimal filtering
    'pharmaceutical': 0.35  # Optimized for pharmaceutical domain
}

def get_similarity_threshold(preset: str = 'pharmaceutical') -> float:
    """Get predefined similarity threshold for different use cases."""
    return SIMILARITY_THRESHOLDS.get(preset, SIMILARITY_THRESHOLDS['pharmaceutical'])

# Example usage in configuration:
"""
# Add to your RAG pipeline:

from similarity_filter import filter_by_similarity_threshold, get_similarity_threshold

# Use in document store or retrieve endpoint:
threshold = get_similarity_threshold('pharmaceutical')  # 0.35

# Apply filtering to results:
filtered_results = filter_by_similarity_threshold(raw_results, threshold)
"""