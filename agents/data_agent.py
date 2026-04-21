"""
Data Agent - Autonomous API monitoring and anomaly detection
"""
from typing import Dict, Any, List
import requests
import time
from datetime import datetime
from agents.base_agent import BaseAgent


class DataAgent(BaseAgent):
    """
    Specialized agent for data operations:
    - Monitor API endpoints
    - Validate data quality
    - Detect anomalies in responses
    - Track performance metrics
    """
    
    def __init__(self):
        """Initialize the Data Agent"""
        super().__init__(
            name="Data Agent",
            role="Monitor APIs, validate data, and detect anomalies"
        )
        self.metrics_history = []
        self.anomalies_detected = []
    
    def monitor_api(self, url: str, expected_status: int = 200) -> Dict[str, Any]:
        """
        Monitor an API endpoint and collect metrics
        
        Args:
            url: API endpoint to monitor
            expected_status: Expected HTTP status code (default 200)
            
        Returns:
            Dictionary with metrics and status
        """
        print(f"📊 Monitoring API: {url}")
        
        metrics = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "status_code": None,
            "response_time_ms": None,
            "error": None
        }
        
        try:
            # Measure response time
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            # Calculate metrics
            response_time_ms = (end_time - start_time) * 1000
            
            metrics.update({
                "success": response.status_code == expected_status,
                "status_code": response.status_code,
                "response_time_ms": round(response_time_ms, 2)
            })
            
            # Store in history
            self.metrics_history.append(metrics)
            
            # Check for anomalies
            anomaly = self.detect_anomaly(metrics)
            if anomaly:
                print(f"⚠️  Anomaly detected: {anomaly}")
                self.anomalies_detected.append({
                    "timestamp": datetime.now().isoformat(),
                    "anomaly": anomaly,
                    "metrics": metrics
                })
            
            if metrics["success"]:
                print(f"✓ API healthy - {response_time_ms:.2f}ms")
            else:
                print(f"❌ Unexpected status: {response.status_code}")
            
            return metrics
            
        except requests.exceptions.Timeout:
            metrics["error"] = "Request timeout"
            print(f"❌ Timeout after 10s")
            return metrics
            
        except requests.exceptions.ConnectionError:
            metrics["error"] = "Connection failed"
            print(f"❌ Connection error")
            return metrics
            
        except Exception as e:
            metrics["error"] = str(e)
            print(f"❌ Error: {str(e)}")
            return metrics
    
    def detect_anomaly(self, current_metrics: Dict[str, Any]) -> str:
        """
        Detect anomalies by comparing current metrics to historical data
        
        Args:
            current_metrics: Latest API monitoring metrics
            
        Returns:
            String describing anomaly, or empty string if none
        """
        # Need at least 3 data points for comparison
        if len(self.metrics_history) < 3:
            return ""
        
        # Only analyze successful requests for baseline
        successful_metrics = [
            m for m in self.metrics_history 
            if m.get("success") and m.get("response_time_ms")
        ]
        
        if len(successful_metrics) < 3:
            return ""
        
        # Calculate average response time from history
        avg_response_time = sum(m["response_time_ms"] for m in successful_metrics) / len(successful_metrics)
        
        current_time = current_metrics.get("response_time_ms")
        
        # Anomaly 1: Response time significantly slower
        if current_time and current_time > avg_response_time * 3:
            return f"Response time {current_time:.2f}ms is 3x slower than average {avg_response_time:.2f}ms"
        
        # Anomaly 2: Status code changed from expected
        if not current_metrics.get("success"):
            return f"Status code {current_metrics.get('status_code')} differs from expected"
        
        # Anomaly 3: Request failed
        if current_metrics.get("error"):
            return f"Request failed: {current_metrics['error']}"
        
        return ""
    
    def run(self, task: str) -> Dict[str, Any]:
        """
        Main autonomous execution - Data Agent's core logic
        
        Args:
            task: Data monitoring task (e.g., "Monitor API health for https://api.example.com")
            
        Returns:
            Dictionary with monitoring results
        """
        print(f"\n{'='*60}")
        print(f"🤖 {self.name} starting task: {task}")
        print(f"{'='*60}\n")
        
        # Step 1: Agent thinks about the task
        thought = self.think(f"What API endpoints should I monitor for this task: {task}")
        print(f"💭 Agent's thought: {thought[:200]}...\n")
        
        # Step 2: Extract API URL from task (simple approach)
        # In production, use tool calling or structured output
        api_url = None
        words = task.split()
        for word in words:
            if word.startswith("http://") or word.startswith("https://"):
                api_url = word.strip(",.;")
                break
        
        if not api_url:
            # Use a default test API if no URL provided
            api_url = "https://httpbin.org/status/200"
            print(f"ℹ️  No URL found in task, using test API: {api_url}\n")
        
        # Step 3: Monitor the API (multiple checks for pattern detection)
        print(f"Starting monitoring of {api_url}...\n")
        
        results = []
        for i in range(3):
            print(f"Check {i+1}/3:")
            metrics = self.monitor_api(api_url)
            results.append(metrics)
            
            if i < 2:  # Don't sleep after last check
                time.sleep(2)  # Wait 2 seconds between checks
            print()
        
        # Step 4: Analyze results with AI
        metrics_summary = "\n".join([
            f"Check {i+1}: Status {m['status_code']}, Time {m['response_time_ms']}ms, Success: {m['success']}"
            for i, m in enumerate(results)
        ])
        
        analysis = self.think(f"Analyze these API monitoring results and provide insights:\n\n{metrics_summary}")
        
        # Step 5: Calculate summary statistics
        successful_checks = sum(1 for r in results if r["success"])
        avg_response_time = sum(r["response_time_ms"] for r in results if r["response_time_ms"]) / len(results) if results else 0
        
        # Step 6: Store in memory
        self.add_to_memory(f"Monitored {api_url}. Success rate: {successful_checks}/{len(results)}")
        
        # Step 7: Return results
        return {
            "status": "success",
            "task": task,
            "api_url": api_url,
            "total_checks": len(results),
            "successful_checks": successful_checks,
            "avg_response_time_ms": round(avg_response_time, 2),
            "anomalies_found": len(self.anomalies_detected),
            "metrics": results,
            "analysis": analysis
        }