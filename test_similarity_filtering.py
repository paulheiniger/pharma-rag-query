#!/usr/bin/env python3
"""
Enhanced retrieve API with similarity threshold filtering

This script provides an enhanced retrieve function that filters out 
low-similarity results to prevent hallucinations in RAG responses.
"""

import requests
import json
from typing import Dict, List, Any, Optional

def call_retrieve_api_with_filtering(
    query: str, 
    k: int = 5,
    similarity_threshold: float = 0.35,
    api_url: str = "http://localhost:8001/v1/retrieve"
) -> Dict[str, Any]:
    """
    Call the retrieve API with similarity threshold filtering.
    
    Args:
        query: Search query
        k: Number of documents to retrieve (before filtering)
        similarity_threshold: Minimum similarity score (0.0-1.0)
        api_url: Retrieve API endpoint
        
    Returns:
        Filtered results with only relevant documents
    """
    # Prepare the request
    request_data = {
        "query": query,
        "k": k  # Get more results than needed for filtering
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 === RETRIEVE API WITH FILTERING ===")
    print(f"📝 Query: '{query}'")
    print(f"📊 Requesting {k} documents")
    print(f"🎯 Similarity threshold: {similarity_threshold}")
    
    try:
        # Call the retrieve API
        response = requests.post(api_url, json=request_data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            results = response.json()
            
            # Apply similarity filtering
            if isinstance(results, list):
                filtered_results = filter_by_similarity(results, similarity_threshold)
                
                print(f"📄 Original results: {len(results)}")
                print(f"✅ Filtered results: {len(filtered_results)}")
                
                # Show similarity scores for debugging
                for i, result in enumerate(filtered_results[:3]):
                    similarity = 1.0 - result.get('dist', 1.0)
                    print(f"   Result {i+1}: similarity = {similarity:.3f}")
                
                return filtered_results
            else:
                print("❌ Unexpected response format")
                return results
                
        else:
            print(f"❌ API Error: {response.status_code}")
            return {"error": f"API returned status {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return {"error": str(e)}

def filter_by_similarity(results: List[Dict[str, Any]], threshold: float) -> List[Dict[str, Any]]:
    """
    Filter results by similarity threshold.
    
    Args:
        results: List of retrieve API results with 'dist' scores
        threshold: Minimum similarity score
        
    Returns:
        Filtered list of relevant results
    """
    filtered_results = []
    
    for result in results:
        # Convert distance to similarity (for cosine: similarity = 1 - distance)
        distance = result.get('dist', 1.0)
        similarity = 1.0 - distance
        
        if similarity >= threshold:
            # Add similarity score for debugging
            result_copy = result.copy()
            result_copy['similarity'] = similarity
            filtered_results.append(result_copy)
        else:
            print(f"🚫 Filtered out result (similarity: {similarity:.3f} < {threshold})")
    
    return filtered_results

def test_similarity_filtering():
    """Test the similarity filtering with different queries."""
    
    test_queries = [
        "banned drugs in India",  # Should return relevant results
        "completely random nonsense blahblah",  # Should filter out most/all results
        "CDSCO drug regulations",  # Should return relevant results
        "unrelated topic about cars"  # Should filter out results
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: '{query}'")
        print('='*60)
        
        results = call_retrieve_api_with_filtering(
            query=query,
            k=5,
            similarity_threshold=0.35
        )
        
        if isinstance(results, list) and len(results) > 0:
            print(f"✅ Found {len(results)} relevant results")
        else:
            print("❌ No relevant results found (good for irrelevant queries!)")

if __name__ == "__main__":
    # Test the filtering
    test_similarity_filtering()