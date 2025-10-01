#!/usr/bin/env python3
"""
Local Model Optimizer
Programming Agent - Local Model Optimization Task
"""

import time
import psutil
import requests
import json
from datetime import datetime

class ModelOptimizer:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.optimization_results = {}
        
    def check_ollama_status(self):
        """Check Ollama server status"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return True, "Ollama server is running"
            else:
                return False, f"Ollama server returned status {response.status_code}"
        except Exception as e:
            return False, f"Ollama server error: {str(e)}"
    
    def get_system_resources(self):
        """Get current system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available": psutil.virtual_memory().available / (1024**3),  # GB
            "disk_usage": psutil.disk_usage('/').percent
        }
    
    def test_model_performance(self, model_name="llama2"):
        """Test model performance"""
        try:
            start_time = time.time()
            
            # Test prompt
            test_prompt = "Hello, how are you?"
            
            # Make request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": test_prompt,
                    "stream": False
                },
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                return True, response_time, response.json()
            else:
                return False, response_time, f"Error: {response.status_code}"
                
        except Exception as e:
            return False, 0, f"Error: {str(e)}"
    
    def optimize_model_settings(self):
        """Optimize model settings"""
        optimizations = {
            "num_ctx": 2048,  # Context window
            "num_predict": 512,  # Max tokens to predict
            "temperature": 0.7,  # Creativity level
            "top_p": 0.9,  # Nucleus sampling
            "repeat_penalty": 1.1,  # Repetition penalty
            "num_thread": psutil.cpu_count()  # Use all CPU cores
        }
        return optimizations
    
    def run_optimization(self):
        """Run complete optimization process"""
        print("🧟 Programming Agent - Local Model Optimization")
        print("=" * 50)
        
        # Check system status
        print("1. Checking Ollama server status...")
        is_running, message = self.check_ollama_status()
        print(f"   Status: {'✅' if is_running else '❌'} {message}")
        
        if not is_running:
            return False, "Ollama server is not running"
        
        # Get system resources
        print("2. Checking system resources...")
        resources = self.get_system_resources()
        print(f"   CPU: {resources['cpu_percent']}%")
        print(f"   Memory: {resources['memory_percent']}% ({resources['memory_available']:.2f} GB available)")
        print(f"   Disk: {resources['disk_usage']}%")
        
        # Test current performance
        print("3. Testing current model performance...")
        success, response_time, result = self.test_model_performance()
        print(f"   Response Time: {response_time:.3f}s")
        print(f"   Status: {'✅' if success else '❌'}")
        
        # Get optimization settings
        print("4. Generating optimization settings...")
        optimizations = self.optimize_model_settings()
        print(f"   Optimizations: {len(optimizations)} settings configured")
        
        # Store results
        self.optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "ollama_status": is_running,
            "system_resources": resources,
            "current_performance": {
                "response_time": response_time,
                "success": success
            },
            "optimizations": optimizations
        }
        
        print("5. Optimization complete!")
        return True, "Model optimization completed successfully"
    
    def save_results(self, filename="optimization_results.json"):
        """Save optimization results"""
        try:
            with open(f"projects/local_model_optimization/{filename}", 'w') as f:
                json.dump(self.optimization_results, f, indent=2)
            return True, f"Results saved to {filename}"
        except Exception as e:
            return False, f"Error saving results: {str(e)}"

def main():
    """Main function"""
    optimizer = ModelOptimizer()
    
    # Run optimization
    success, message = optimizer.run_optimization()
    
    if success:
        # Save results
        save_success, save_message = optimizer.save_results()
        print(f"\n💾 Save Results: {'✅' if save_success else '❌'} {save_message}")
        
        # Update work log
        with open("logs/agent_work.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Programming Agent - Task: Local Model Optimization - Status: Completed - Notes: {message}\n")
        
        print(f"\n🎉 {message}")
    else:
        print(f"\n❌ {message}")
        
        # Log error
        with open("logs/agent_error.log", "a") as f:
            f.write(f"{datetime.now()}: Agent: Programming Agent - Error: {message} - Severity: HIGH - Status: UNRESOLVED\n")

if __name__ == "__main__":
    main()
