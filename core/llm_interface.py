"""
LLM Interface for SecAgent - Handles communication with various LLM providers
"""
import openai
import anthropic
import asyncio
import json
from typing import Dict, List, Optional, Any
from config import Config

class LLMInterface:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if Config.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        
        if Config.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    async def query_llm(self, prompt: str, model: str = None, system_prompt: str = None) -> str:
        """Query LLM with given prompt"""
        if not model:
            model = Config.DEFAULT_MODEL
        
        try:
            if model.startswith("gpt") and self.openai_client:
                return self._query_openai(prompt, model, system_prompt)
            elif model.startswith("claude") and self.anthropic_client:
                return self._query_anthropic(prompt, model, system_prompt)
            else:
                raise ValueError(f"Model {model} not supported or API key not configured")
        except Exception as e:
            return f"Error querying LLM: {str(e)}"
    
    def _query_openai(self, prompt: str, model: str, system_prompt: str = None) -> str:
        """Query OpenAI GPT models"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def _query_anthropic(self, prompt: str, model: str, system_prompt: str = None) -> str:
        """Query Anthropic Claude models"""
        message = self.anthropic_client.messages.create(
            model=model,
            max_tokens=1500,
            temperature=0.3,
            system=system_prompt or "You are a helpful cybersecurity assistant.",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def generate_payload(self, vulnerability_type: str, target_info: Dict) -> str:
        """Generate exploit payload using LLM"""
        system_prompt = """You are a cybersecurity expert specializing in penetration testing. 
        Generate appropriate payloads for testing purposes only. Always include disclaimers about authorized use."""
        
        prompt = f"""
        Generate a payload for testing {vulnerability_type} vulnerability.
        Target information: {json.dumps(target_info, indent=2)}
        
        Requirements:
        1. Provide educational/testing payload only
        2. Include explanation of how it works
        3. Add proper disclaimers
        4. Suggest mitigation strategies
        """
        
        return asyncio.run(self.query_llm(prompt, system_prompt=system_prompt))
    
    def analyze_vulnerability(self, scan_results: Dict) -> str:
        """Analyze scan results and suggest attack vectors"""
        system_prompt = """You are a penetration testing expert. Analyze scan results and provide 
        professional security assessment with potential attack vectors and remediation advice."""
        
        prompt = f"""
        Analyze these scan results and provide:
        1. Identified vulnerabilities and their severity
        2. Potential attack vectors
        3. Exploitation difficulty assessment
        4. Recommended remediation steps
        
        Scan Results:
        {json.dumps(scan_results, indent=2)}
        """
        
        return asyncio.run(self.query_llm(prompt, system_prompt=system_prompt))
    
    def generate_social_engineering_template(self, target_info: Dict, campaign_type: str) -> str:
        """Generate social engineering templates for authorized testing"""
        system_prompt = """You are a social engineering awareness trainer. Create educational 
        templates for authorized security awareness testing only."""
        
        prompt = f"""
        Create a {campaign_type} template for security awareness testing.
        Target context: {json.dumps(target_info, indent=2)}
        
        Requirements:
        1. Professional and believable content
        2. Include red flags for training purposes
        3. Provide detection tips
        4. Emphasize this is for authorized testing only
        """
        
        return asyncio.run(self.query_llm(prompt, system_prompt=system_prompt))
