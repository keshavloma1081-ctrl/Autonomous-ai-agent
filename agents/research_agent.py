"""
Research Agent - Autonomous ML research and paper analysis
"""
from typing import Dict, Any, List
import requests
from agents.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """
    Specialized agent for ML research tasks:
    - Search for papers on arXiv
    - Summarize state-of-the-art (SOTA) techniques
    - Track research trends
    """
    
    def __init__(self):
        """Initialize the Research Agent"""
        super().__init__(
            name="Research Agent",
            role="Find, analyze, and summarize ML research papers and trends"
        )
        self.arxiv_base_url = "http://export.arxiv.org/api/query"
    
    def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search arXiv for papers matching the query
        
        Args:
            query: Search terms (e.g., "transformer attention mechanisms")
            max_results: Maximum number of papers to return
            
        Returns:
            List of paper dictionaries with title, authors, summary, link
        """
        print(f"🔍 Searching arXiv for: {query}")
        
        import time
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Build API request parameters
                params = {
                    "search_query": f"all:{query}",
                    "start": 0,
                    "max_results": max_results,
                    "sortBy": "relevance",
                    "sortOrder": "descending"
                }
                
                # Add user agent to avoid blocking
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                # Make request to arXiv API
                response = requests.get(
                    self.arxiv_base_url, 
                    params=params, 
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                
                # Parse the XML response
                papers = self._parse_arxiv_response(response.text)
                
                print(f"✓ Found {len(papers)} papers")
                return papers
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⏳ Rate limited. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Error searching arXiv: {str(e)}")
                    return []
            except Exception as e:
                print(f"❌ Error searching arXiv: {str(e)}")
                return []
        
        return []
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """
        Parse arXiv XML response into clean paper data
        
        Args:
            xml_text: Raw XML response from arXiv API
            
        Returns:
            List of parsed paper dictionaries
        """
        import xml.etree.ElementTree as ET
        
        papers = []
        
        try:
            # Parse XML
            root = ET.fromstring(xml_text)
            
            # arXiv uses Atom namespace
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            # Find all entry elements (each is a paper)
            entries = root.findall('atom:entry', namespace)
            
            for entry in entries:
                # Extract paper data
                title = entry.find('atom:title', namespace)
                summary = entry.find('atom:summary', namespace)
                link = entry.find('atom:id', namespace)
                published = entry.find('atom:published', namespace)
                
                # Get authors
                authors = []
                for author in entry.findall('atom:author', namespace):
                    name = author.find('atom:name', namespace)
                    if name is not None:
                        authors.append(name.text.strip())
                
                # Build paper dictionary
                paper = {
                    "title": title.text.strip() if title is not None else "No title",
                    "summary": summary.text.strip() if summary is not None else "No summary",
                    "link": link.text.strip() if link is not None else "",
                    "published": published.text.strip() if published is not None else "",
                    "authors": authors
                }
                
                papers.append(paper)
        
        except Exception as e:
            print(f"Error parsing XML: {str(e)}")
        
        return papers
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Main autonomous execution - Research Agent's core logic
        
        Args:
            task: Research task (e.g., "Find recent papers on transformers")
            
        Returns:
            Dictionary with research results
        """
        print(f"\n{'='*60}")
        print(f"🤖 {self.name} starting task: {task}")
        print(f"{'='*60}\n")
        
        # Step 1: Agent thinks about the task
        thought = self.think(f"What search query should I use for this task: {task}")
        print(f"💭 Agent's thought: {thought[:200]}...\n")
        
        # Step 2: Extract search query from thought (simple approach)
        # In production, use tool calling or structured output
        search_query = task.split("about")[-1].strip() if "about" in task.lower() else task
        
        # Step 3: Search for papers
        papers = self.search_papers(search_query, max_results=5)
        
        if not papers:
            return {
                "status": "failure",
                "message": "No papers found",
                "task": task
            }
        
        # Step 4: Analyze and summarize findings
        papers_summary = "\n\n".join([
            f"Paper {i+1}: {p['title']}\nAuthors: {', '.join(p['authors'][:3])}\nSummary: {p['summary'][:200]}..."
            for i, p in enumerate(papers)
        ])
        
        analysis = self.think(f"Analyze these papers and provide key insights:\n\n{papers_summary}")
        
        # Step 5: Store in memory
        self.add_to_memory(f"Researched: {task}. Found {len(papers)} papers.")
        
        # Step 6: Return results
        return {
            "status": "success",
            "task": task,
            "papers_found": len(papers),
            "papers": papers,
            "analysis": analysis
        }