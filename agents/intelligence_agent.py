"""
Intelligence Agent - Autonomous web scraping and trend analysis
"""
from typing import Dict, Any, List
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from agents.base_agent import BaseAgent


class IntelligenceAgent(BaseAgent):
    """
    Specialized agent for competitive intelligence:
    - Scrape web pages for data
    - Extract key information
    - Track trends and changes
    - Competitive analysis
    """
    
    def __init__(self):
        """Initialize the Intelligence Agent"""
        super().__init__(
            name="Intelligence Agent",
            role="Gather competitive intelligence, track trends, and analyze web data"
        )
        self.scraped_data = []
        self.trends = []
    
    def scrape_webpage(self, url: str) -> Dict[str, Any]:
        """
        Scrape a webpage and extract key information
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary with scraped data
        """
        print(f"🌐 Scraping: {url}")
        
        result = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "title": None,
            "headings": [],
            "paragraphs": [],
            "links": [],
            "error": None
        }
        
        try:
            # Make request with user agent
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            result["title"] = title.get_text().strip() if title else "No title"
            
            # Extract headings (h1, h2, h3)
            headings = []
            for tag in ['h1', 'h2', 'h3']:
                for heading in soup.find_all(tag):
                    text = heading.get_text().strip()
                    if text:
                        headings.append({"tag": tag, "text": text})
            result["headings"] = headings[:10]  # Limit to top 10
            
            # Extract paragraphs
            paragraphs = []
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if text and len(text) > 50:  # Only substantial paragraphs
                    paragraphs.append(text)
            result["paragraphs"] = paragraphs[:5]  # Limit to top 5
            
            # Extract links
            links = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                text = a.get_text().strip()
                if href.startswith('http') and text:
                    links.append({"url": href, "text": text})
            result["links"] = links[:10]  # Limit to top 10
            
            result["success"] = True
            self.scraped_data.append(result)
            
            print(f"✓ Scraped successfully - Title: {result['title'][:50]}...")
            return result
            
        except requests.exceptions.Timeout:
            result["error"] = "Request timeout"
            print(f"❌ Timeout after 10s")
            return result
            
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection failed"
            print(f"❌ Connection error")
            return result
            
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ Error: {str(e)}")
            return result
    
    def extract_insights(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key insights from scraped data
        
        Args:
            scraped_data: Dictionary with scraped webpage data
            
        Returns:
            Dictionary with extracted insights
        """
        insights = {
            "url": scraped_data["url"],
            "key_topics": [],
            "summary": "",
            "notable_links": []
        }
        
        # Extract key topics from headings
        if scraped_data.get("headings"):
            topics = [h["text"] for h in scraped_data["headings"][:5]]
            insights["key_topics"] = topics
        
        # Create brief summary from first paragraph
        if scraped_data.get("paragraphs"):
            insights["summary"] = scraped_data["paragraphs"][0][:200] + "..."
        
        # Notable external links
        if scraped_data.get("links"):
            insights["notable_links"] = [
                link["text"] for link in scraped_data["links"][:3]
            ]
        
        return insights
    
    def detect_trends(self, current_data: Dict[str, Any]) -> List[str]:
        """
        Detect trends by comparing current data to historical scrapes
        
        Args:
            current_data: Latest scraped data
            
        Returns:
            List of detected trends/changes
        """
        trends = []
        
        # Need historical data for comparison
        if len(self.scraped_data) < 2:
            return ["Baseline data collected - need more scrapes for trend detection"]
        
        # Compare with previous scrapes of same URL
        previous_scrapes = [
            d for d in self.scraped_data[:-1]  # Exclude current
            if d.get("url") == current_data.get("url") and d.get("success")
        ]
        
        if not previous_scrapes:
            return ["First scrape of this URL - no trends yet"]
        
        # Compare headings
        prev_headings = set(h["text"] for h in previous_scrapes[-1].get("headings", []))
        curr_headings = set(h["text"] for h in current_data.get("headings", []))
        
        new_headings = curr_headings - prev_headings
        if new_headings:
            trends.append(f"New topics detected: {', '.join(list(new_headings)[:3])}")
        
        # Compare number of paragraphs (content volume)
        prev_para_count = len(previous_scrapes[-1].get("paragraphs", []))
        curr_para_count = len(current_data.get("paragraphs", []))
        
        if curr_para_count > prev_para_count * 1.5:
            trends.append(f"Content volume increased significantly ({prev_para_count} → {curr_para_count} paragraphs)")
        elif curr_para_count < prev_para_count * 0.5:
            trends.append(f"Content volume decreased ({prev_para_count} → {curr_para_count} paragraphs)")
        
        if not trends:
            trends.append("No significant changes detected")
        
        return trends
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Main autonomous execution - Intelligence Agent's core logic
        
        Args:
            task: Intelligence gathering task (e.g., "Analyze competitor website https://example.com")
            
        Returns:
            Dictionary with intelligence results
        """
        print(f"\n{'='*60}")
        print(f"🤖 {self.name} starting task: {task}")
        print(f"{'='*60}\n")
        
        # Step 1: Agent thinks about the task
        thought = self.think(f"What website should I analyze for this task: {task}")
        print(f"💭 Agent's thought: {thought[:200]}...\n")
        
        # Step 2: Extract URL from task
        target_url = None
        words = task.split()
        for word in words:
            if word.startswith("http://") or word.startswith("https://"):
                target_url = word.strip(",.;")
                break
        
        if not target_url:
            # Use a default demo URL
            target_url = "https://news.ycombinator.com/"
            print(f"ℹ️  No URL found in task, using demo: {target_url}\n")
        
        # Step 3: Scrape the website
        print(f"Starting intelligence gathering on {target_url}...\n")
        scraped = self.scrape_webpage(target_url)
        
        if not scraped["success"]:
            return {
                "status": "failure",
                "message": f"Failed to scrape: {scraped.get('error')}",
                "task": task
            }
        
        # Step 4: Extract insights
        insights = self.extract_insights(scraped)
        
        # Step 5: Detect trends
        trends = self.detect_trends(scraped)
        
        # Step 6: AI analysis of findings
        analysis_prompt = f"""Analyze this competitive intelligence:
        
Title: {scraped['title']}
Key Topics: {', '.join(insights['key_topics'])}
Summary: {insights['summary']}

Provide strategic insights and recommendations."""
        
        analysis = self.think(analysis_prompt)
        
        # Step 7: Store in memory
        self.add_to_memory(f"Analyzed {target_url}. Found {len(scraped['headings'])} topics.")
        
        # Step 8: Return results
        return {
            "status": "success",
            "task": task,
            "url": target_url,
            "title": scraped["title"],
            "key_topics": insights["key_topics"],
            "summary": insights["summary"],
            "trends": trends,
            "analysis": analysis,
            "scraped_data": scraped
        }