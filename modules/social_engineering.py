"""
Social Engineering Module - OSINT and social engineering capabilities
"""
import requests
import json
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from core.llm_interface import LLMInterface
from config import Config

class SocialEngineeringModule:
    def __init__(self):
        self.llm = LLMInterface()
        self.session = requests.Session()
        
    def email_enumeration(self, domain: str) -> List[str]:
        """Enumerate email addresses for a domain"""
        emails = set()
        
        # Common email patterns
        common_patterns = [
            "info@{domain}",
            "admin@{domain}",
            "support@{domain}",
            "contact@{domain}",
            "sales@{domain}",
            "hr@{domain}",
            "security@{domain}",
            "webmaster@{domain}"
        ]
        
        for pattern in common_patterns:
            emails.add(pattern.format(domain=domain))
        
        # Search engines and social media scraping would go here
        # For demo purposes, we'll simulate some discovered emails
        simulated_emails = [
            f"john.doe@{domain}",
            f"jane.smith@{domain}",
            f"admin@{domain}",
            f"support@{domain}"
        ]
        
        emails.update(simulated_emails)
        return list(emails)
    
    def linkedin_reconnaissance(self, company_name: str) -> Dict:
        """Gather information from LinkedIn (simulated)"""
        # In a real implementation, this would use LinkedIn API or scraping
        # For demo purposes, we'll simulate the data
        
        results = {
            'company_info': {
                'name': company_name,
                'industry': 'Technology',
                'size': '100-500 employees',
                'location': 'Various locations'
            },
            'employees': [
                {
                    'name': 'John Doe',
                    'position': 'IT Manager',
                    'department': 'Information Technology',
                    'tenure': '3 years'
                },
                {
                    'name': 'Jane Smith',
                    'position': 'Security Analyst',
                    'department': 'Cybersecurity',
                    'tenure': '2 years'
                },
                {
                    'name': 'Mike Johnson',
                    'position': 'System Administrator',
                    'department': 'IT Operations',
                    'tenure': '5 years'
                }
            ],
            'technologies': [
                'Microsoft Office 365',
                'AWS',
                'Salesforce',
                'Slack'
            ]
        }
        
        return results
    
    def generate_spear_phishing_email(self, target_info: Dict, campaign_type: str) -> str:
        """Generate spear phishing email using LLM"""
        system_prompt = """You are a cybersecurity professional creating educational spear phishing examples 
        for authorized security awareness training. Create realistic but clearly marked training content."""
        
        prompt = f"""
        Create a spear phishing email for security awareness training with the following details:
        
        Target Information: {json.dumps(target_info, indent=2)}
        Campaign Type: {campaign_type}
        
        Requirements:
        1. Make it realistic and convincing
        2. Include clear "[TRAINING EXERCISE]" markers
        3. Explain the social engineering techniques used
        4. Provide detection tips for recipients
        5. Include a disclaimer about authorized training use only
        
        The email should demonstrate common tactics like urgency, authority, or familiarity.
        """
        
        return asyncio.run(self.llm.query_llm(prompt, system_prompt=system_prompt))
    
    def password_policy_analysis(self, domain: str) -> Dict:
        """Analyze password policies and generate targeted wordlists"""
        # Simulate password policy discovery
        policy_info = {
            'minimum_length': 8,
            'requires_uppercase': True,
            'requires_lowercase': True,
            'requires_numbers': True,
            'requires_special_chars': False,
            'common_patterns': [
                f"{domain.split('.')[0]}2024!",
                f"{domain.split('.')[0]}123",
                "Password123",
                "Welcome123"
            ]
        }
        
        # Generate targeted wordlist based on company info
        wordlist = [
            f"{domain.split('.')[0]}2024",
            f"{domain.split('.')[0]}123",
            f"{domain.split('.')[0]}!",
            "Password123",
            "Welcome123",
            "Admin123",
            "Spring2024",
            "Summer2024",
            "Company123"
        ]
        
        return {
            'policy': policy_info,
            'targeted_wordlist': wordlist
        }
    
    def social_media_osint(self, target_name: str, company: str) -> Dict:
        """Gather OSINT from social media platforms"""
        # Simulated social media intelligence gathering
        results = {
            'platforms_found': ['LinkedIn', 'Twitter', 'Facebook'],
            'personal_info': {
                'interests': ['Technology', 'Cybersecurity', 'Coffee'],
                'location': 'San Francisco, CA',
                'education': 'University of California',
                'connections': 500
            },
            'professional_info': {
                'current_role': 'IT Manager',
                'company': company,
                'skills': ['Network Security', 'Cloud Computing', 'Project Management'],
                'certifications': ['CISSP', 'AWS Certified']
            },
            'potential_vectors': [
                'Professional development opportunities',
                'Industry conferences and events',
                'Technology updates and patches',
                'Company policy changes'
            ]
        }
        
        return results
    
    def generate_pretext_scenarios(self, target_info: Dict) -> List[Dict]:
        """Generate pretext scenarios for social engineering"""
        scenarios = [
            {
                'type': 'IT Support',
                'scenario': 'Urgent security update required',
                'approach': 'Call claiming to be from IT support needing to verify credentials for a critical security patch',
                'urgency': 'High',
                'authority': 'IT Department',
                'social_proof': 'Other employees have already completed this process'
            },
            {
                'type': 'HR Request',
                'scenario': 'Employee verification process',
                'approach': 'Email from HR requesting verification of personal information for annual review',
                'urgency': 'Medium',
                'authority': 'Human Resources',
                'social_proof': 'Company-wide initiative'
            },
            {
                'type': 'Vendor Impersonation',
                'scenario': 'Service provider maintenance',
                'approach': 'Impersonate a known vendor requiring system access for maintenance',
                'urgency': 'Medium',
                'authority': 'Trusted Vendor',
                'social_proof': 'Scheduled maintenance window'
            },
            {
                'type': 'Executive Impersonation',
                'scenario': 'Urgent business request',
                'approach': 'Email from executive requesting immediate action on confidential matter',
                'urgency': 'Critical',
                'authority': 'C-Level Executive',
                'social_proof': 'Time-sensitive business opportunity'
            }
        ]
        
        return scenarios
    
    def vishing_script_generator(self, target_info: Dict, scenario: str) -> str:
        """Generate voice phishing (vishing) scripts"""
        system_prompt = """You are creating educational vishing scripts for authorized security awareness training. 
        Include clear training markers and educational content."""
        
        prompt = f"""
        Create a vishing (voice phishing) script for security awareness training:
        
        Target Information: {json.dumps(target_info, indent=2)}
        Scenario: {scenario}
        
        Requirements:
        1. Create a realistic phone conversation script
        2. Include psychological manipulation techniques
        3. Mark clearly as "[TRAINING EXERCISE]"
        4. Explain the techniques being demonstrated
        5. Provide guidance on how to recognize and respond to such calls
        6. Include proper disclaimers about authorized training use
        
        The script should demonstrate common vishing tactics like urgency, authority, and social proof.
        """
        
        return asyncio.run(self.llm.query_llm(prompt, system_prompt=system_prompt))
    
    def physical_security_assessment(self, target_location: str) -> Dict:
        """Assess physical security measures (simulated)"""
        # Simulated physical security assessment
        assessment = {
            'location': target_location,
            'security_measures': {
                'access_control': 'Badge reader at main entrance',
                'security_guards': 'Present during business hours',
                'cameras': 'CCTV coverage of main areas',
                'visitor_management': 'Sign-in process required'
            },
            'potential_weaknesses': [
                'Tailgating opportunities at main entrance',
                'Unsecured side entrances',
                'Dumpster diving opportunities',
                'Social engineering of reception staff'
            ],
            'recommended_tests': [
                'Badge cloning attempt',
                'Tailgating test',
                'Social engineering of staff',
                'Physical penetration test'
            ]
        }
        
        return assessment
    
    async def comprehensive_social_engineering_assessment(self, target_company: str, target_domain: str) -> Dict:
        """Perform comprehensive social engineering assessment"""
        print(f"[+] Starting social engineering assessment for {target_company}")
        
        results = {
            'target_company': target_company,
            'target_domain': target_domain,
            'timestamp': asyncio.get_event_loop().time(),
            'email_enumeration': [],
            'linkedin_recon': {},
            'social_media_osint': {},
            'password_analysis': {},
            'pretext_scenarios': [],
            'phishing_templates': [],
            'vishing_scripts': [],
            'physical_assessment': {},
            'llm_recommendations': ""
        }
        
        # Email enumeration
        print("[+] Enumerating email addresses...")
        results['email_enumeration'] = self.email_enumeration(target_domain)
        
        # LinkedIn reconnaissance
        print("[+] Gathering LinkedIn intelligence...")
        results['linkedin_recon'] = self.linkedin_reconnaissance(target_company)
        
        # Social media OSINT
        print("[+] Conducting social media OSINT...")
        key_employees = results['linkedin_recon'].get('employees', [])
        if key_employees:
            results['social_media_osint'] = self.social_media_osint(
                key_employees[0]['name'], 
                target_company
            )
        
        # Password policy analysis
        print("[+] Analyzing password policies...")
        results['password_analysis'] = self.password_policy_analysis(target_domain)
        
        # Generate pretext scenarios
        print("[+] Generating pretext scenarios...")
        results['pretext_scenarios'] = self.generate_pretext_scenarios(results)
        
        # Generate phishing templates
        print("[+] Creating phishing templates...")
        for scenario in results['pretext_scenarios'][:2]:  # Limit for demo
            template = self.generate_spear_phishing_email(results, scenario['type'])
            results['phishing_templates'].append({
                'scenario': scenario['type'],
                'template': template
            })
        
        # Generate vishing scripts
        print("[+] Creating vishing scripts...")
        vishing_script = self.vishing_script_generator(results, "IT Support")
        results['vishing_scripts'].append({
            'scenario': 'IT Support',
            'script': vishing_script
        })
        
        # Physical security assessment
        print("[+] Assessing physical security...")
        results['physical_assessment'] = self.physical_security_assessment(f"{target_company} Headquarters")
        
        # LLM analysis and recommendations
        print("[+] Generating LLM recommendations...")
        results['llm_recommendations'] = self.llm.analyze_vulnerability(results)
        
        return results
