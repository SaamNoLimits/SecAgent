"""
Reconnaissance Module - Information gathering and OSINT capabilities
"""
import nmap
import requests
import dns.resolver
import whois
import socket
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import json
import subprocess
from config import Config
from core.llm_interface import LLMInterface

class ReconModule:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.llm = LLMInterface()
        self.session = requests.Session()
        
    def port_scan(self, target: str, ports: str = None) -> Dict:
        """Perform port scanning using nmap"""
        try:
            if not ports:
                ports = ','.join(map(str, Config.COMMON_PORTS))
            
            print(f"[+] Scanning {target} on ports {ports}")
            self.nm.scan(target, ports, arguments='-sS -sV -O --script=vuln')
            
            results = {}
            for host in self.nm.all_hosts():
                results[host] = {
                    'state': self.nm[host].state(),
                    'protocols': {},
                    'os': self.nm[host].get('osmatch', []),
                    'hostnames': self.nm[host].get('hostnames', [])
                }
                
                for protocol in self.nm[host].all_protocols():
                    ports_info = {}
                    for port in self.nm[host][protocol].keys():
                        port_info = self.nm[host][protocol][port]
                        ports_info[port] = {
                            'state': port_info['state'],
                            'name': port_info['name'],
                            'product': port_info.get('product', ''),
                            'version': port_info.get('version', ''),
                            'extrainfo': port_info.get('extrainfo', ''),
                            'script': port_info.get('script', {})
                        }
                    results[host]['protocols'][protocol] = ports_info
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def subdomain_enumeration(self, domain: str) -> List[str]:
        """Enumerate subdomains using various techniques"""
        subdomains = set()
        
        # Dictionary-based enumeration
        for subdomain in Config.COMMON_SUBDOMAINS:
            try:
                full_domain = f"{subdomain}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.add(full_domain)
            except socket.gaierror:
                pass
        
        # DNS zone transfer attempt
        try:
            ns_records = dns.resolver.resolve(domain, 'NS')
            for ns in ns_records:
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ns), domain))
                    for name in zone.nodes.keys():
                        subdomains.add(f"{name}.{domain}")
                except:
                    pass
        except:
            pass
        
        return list(subdomains)
    
    def whois_lookup(self, domain: str) -> Dict:
        """Perform WHOIS lookup"""
        try:
            w = whois.whois(domain)
            return {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'emails': w.emails,
                'org': w.org,
                'country': w.country
            }
        except Exception as e:
            return {'error': str(e)}
    
    async def web_crawl(self, url: str, depth: int = 2) -> Dict:
        """Crawl website and gather information"""
        crawled_urls = set()
        forms = []
        technologies = set()
        
        async def crawl_page(session, url, current_depth):
            if current_depth > depth or url in crawled_urls:
                return
            
            crawled_urls.add(url)
            
            try:
                async with session.get(url, timeout=10) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract forms
                    for form in soup.find_all('form'):
                        form_data = {
                            'action': form.get('action', ''),
                            'method': form.get('method', 'GET'),
                            'inputs': []
                        }
                        for input_tag in form.find_all('input'):
                            form_data['inputs'].append({
                                'name': input_tag.get('name', ''),
                                'type': input_tag.get('type', 'text'),
                                'value': input_tag.get('value', '')
                            })
                        forms.append(form_data)
                    
                    # Technology detection
                    for script in soup.find_all('script', src=True):
                        src = script.get('src', '')
                        if 'jquery' in src.lower():
                            technologies.add('jQuery')
                        elif 'angular' in src.lower():
                            technologies.add('AngularJS')
                        elif 'react' in src.lower():
                            technologies.add('React')
                    
                    # Find more URLs to crawl
                    if current_depth < depth:
                        for link in soup.find_all('a', href=True):
                            href = link.get('href')
                            if href.startswith('/'):
                                new_url = f"{url.rstrip('/')}{href}"
                                await crawl_page(session, new_url, current_depth + 1)
                            elif href.startswith('http') and url in href:
                                await crawl_page(session, href, current_depth + 1)
                                
            except Exception as e:
                print(f"Error crawling {url}: {e}")
        
        async with aiohttp.ClientSession() as session:
            await crawl_page(session, url, 0)
        
        return {
            'crawled_urls': list(crawled_urls),
            'forms': forms,
            'technologies': list(technologies)
        }
    
    def dns_enumeration(self, domain: str) -> Dict:
        """Comprehensive DNS enumeration"""
        results = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                results[record_type] = [str(answer) for answer in answers]
            except Exception as e:
                results[record_type] = f"Error: {str(e)}"
        
        return results
    
    async def comprehensive_recon(self, target: str) -> Dict:
        """Perform comprehensive reconnaissance"""
        print(f"[+] Starting comprehensive reconnaissance on {target}")
        
        results = {
            'target': target,
            'timestamp': asyncio.get_event_loop().time(),
            'port_scan': {},
            'subdomains': [],
            'whois': {},
            'dns': {},
            'web_crawl': {},
            'llm_analysis': ""
        }
        
        # Port scanning
        results['port_scan'] = self.port_scan(target)
        
        # Subdomain enumeration
        results['subdomains'] = self.subdomain_enumeration(target)
        
        # WHOIS lookup
        results['whois'] = self.whois_lookup(target)
        
        # DNS enumeration
        results['dns'] = self.dns_enumeration(target)
        
        # Web crawling (if web services detected)
        if any(port in [80, 443, 8080, 8443] for port_info in results['port_scan'].values() 
               for protocol in port_info.get('protocols', {}).values() 
               for port in protocol.keys()):
            web_url = f"http://{target}"
            results['web_crawl'] = await self.web_crawl(web_url)
        
        # LLM analysis of results
        results['llm_analysis'] = self.llm.analyze_vulnerability(results)
        
        return results
