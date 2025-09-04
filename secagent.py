#!/usr/bin/env python3
"""
SecAgent - AI-Powered Red Team Penetration Testing Assistant

A comprehensive penetration testing framework that leverages Large Language Models (LLMs)
to automate and enhance security assessments, vulnerability analysis, and exploitation.

Author: SecAgent Development Team
Version: 1.0
License: Educational Use Only

DISCLAIMER: This tool is for authorized penetration testing and educational purposes only.
Unauthorized use is strictly prohibited and may be illegal.
"""

import asyncio
import click
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import our modules
from config import Config
from core.llm_interface import LLMInterface
from modules.reconnaissance import ReconModule
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.exploitation import ExploitationModule
from modules.social_engineering import SocialEngineeringModule
from modules.reporting import ReportingModule

console = Console()

class SecAgent:
    def __init__(self):
        self.llm = LLMInterface()
        self.recon = ReconModule()
        self.vuln_scanner = VulnerabilityScanner()
        self.exploit = ExploitationModule()
        self.social_eng = SocialEngineeringModule()
        self.reporter = ReportingModule()
        
        self.assessment_data = {}
        
    def display_banner(self):
        """Display SecAgent banner"""
        banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ███████╗███████╗ ██████╗ █████╗  ██████╗ ███████╗███╗   ██╗████████╗       ║
║   ██╔════╝██╔════╝██╔════╝██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝       ║
║   ███████╗█████╗  ██║     ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║          ║
║   ╚════██║██╔══╝  ██║     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║          ║
║   ███████║███████╗╚██████╗██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║          ║
║   ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝          ║
║                                                                               ║
║                   AI-Powered Red Team Penetration Testing Assistant          ║
║                                                                               ║
║                        🛡️  For Authorized Testing Only  🛡️                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.YELLOW}⚠️  LEGAL DISCLAIMER ⚠️{Style.RESET_ALL}
This tool is designed for authorized penetration testing and educational purposes only.
Users must have explicit written permission before testing any systems.
Unauthorized use is strictly prohibited and may violate local and international laws.

{Fore.GREEN}🚀 Features:{Style.RESET_ALL}
• AI-Enhanced Reconnaissance & OSINT
• Automated Vulnerability Scanning
• LLM-Powered Exploit Generation
• Social Engineering Assessment
• Comprehensive Reporting
• Multi-LLM Support (GPT-4, Claude)

{Fore.BLUE}Version: 1.0 | Author: SecAgent Team{Style.RESET_ALL}
"""
        print(banner)
    
    def check_prerequisites(self):
        """Check if required API keys and dependencies are configured"""
        issues = []
        
        if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
            issues.append("❌ No LLM API keys configured (OpenAI or Anthropic required)")
        
        if Config.OPENAI_API_KEY:
            console.print("✅ OpenAI API key configured", style="green")
        
        if Config.ANTHROPIC_API_KEY:
            console.print("✅ Anthropic API key configured", style="green")
        
        if issues:
            console.print("\n[red]Configuration Issues Found:[/red]")
            for issue in issues:
                console.print(f"  {issue}")
            console.print("\n[yellow]Please configure API keys in your .env file or environment variables.[/yellow]")
            return False
        
        return True
    
    async def run_reconnaissance(self, target: str) -> dict:
        """Run comprehensive reconnaissance"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running reconnaissance...", total=None)
            
            try:
                results = await self.recon.comprehensive_recon(target)
                self.assessment_data['reconnaissance'] = results
                progress.update(task, description="✅ Reconnaissance completed")
                return results
            except Exception as e:
                progress.update(task, description=f"❌ Reconnaissance failed: {str(e)}")
                return {'error': str(e)}
    
    async def run_vulnerability_scan(self, target: str, forms: list = None) -> dict:
        """Run vulnerability scanning"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running vulnerability scan...", total=None)
            
            try:
                results = await self.vuln_scanner.comprehensive_scan(target, forms)
                self.assessment_data['vulnerability_scan'] = results
                progress.update(task, description="✅ Vulnerability scan completed")
                return results
            except Exception as e:
                progress.update(task, description=f"❌ Vulnerability scan failed: {str(e)}")
                return {'error': str(e)}
    
    async def run_exploitation(self, vuln_results: dict) -> dict:
        """Run exploitation attempts"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running exploitation...", total=None)
            
            try:
                results = await self.exploit.automated_exploitation(vuln_results)
                self.assessment_data['exploitation'] = results
                progress.update(task, description="✅ Exploitation completed")
                return results
            except Exception as e:
                progress.update(task, description=f"❌ Exploitation failed: {str(e)}")
                return {'error': str(e)}
    
    async def run_social_engineering(self, company: str, domain: str) -> dict:
        """Run social engineering assessment"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running social engineering assessment...", total=None)
            
            try:
                results = await self.social_eng.comprehensive_social_engineering_assessment(company, domain)
                self.assessment_data['social_engineering'] = results
                progress.update(task, description="✅ Social engineering assessment completed")
                return results
            except Exception as e:
                progress.update(task, description=f"❌ Social engineering assessment failed: {str(e)}")
                return {'error': str(e)}
    
    async def generate_report(self) -> dict:
        """Generate comprehensive report"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating report...", total=None)
            
            try:
                results = await self.reporter.generate_comprehensive_report(self.assessment_data)
                progress.update(task, description="✅ Report generated")
                return results
            except Exception as e:
                progress.update(task, description=f"❌ Report generation failed: {str(e)}")
                return {'error': str(e)}
    
    def display_results_summary(self, results: dict):
        """Display results summary in a nice table"""
        if 'vulnerabilities' in results:
            vulns = results['vulnerabilities']
            
            if vulns:
                table = Table(title="🔍 Vulnerabilities Found")
                table.add_column("Type", style="cyan")
                table.add_column("Severity", style="magenta")
                table.add_column("Target", style="green")
                table.add_column("Evidence", style="yellow")
                
                for vuln in vulns[:10]:  # Show top 10
                    severity_style = {
                        'Critical': 'red bold',
                        'High': 'red',
                        'Medium': 'yellow',
                        'Low': 'green'
                    }.get(vuln.get('severity', 'Medium'), 'white')
                    
                    table.add_row(
                        vuln.get('type', 'Unknown'),
                        vuln.get('severity', 'Medium'),
                        vuln.get('url', vuln.get('target', 'N/A'))[:50],
                        vuln.get('evidence', 'N/A')[:30]
                    )
                
                console.print(table)
            else:
                console.print("✅ No vulnerabilities found!", style="green bold")

# CLI Commands
@click.group()
@click.version_option(version='1.0')
def cli():
    """SecAgent - AI-Powered Red Team Penetration Testing Assistant"""
    pass

@cli.command()
def banner():
    """Display SecAgent banner and information"""
    agent = SecAgent()
    agent.display_banner()

@cli.command()
@click.option('--target', '-t', required=True, help='Target IP address or domain')
@click.option('--output', '-o', help='Output file for results')
def recon(target, output):
    """Run comprehensive reconnaissance on target"""
    agent = SecAgent()
    agent.display_banner()
    
    if not agent.check_prerequisites():
        sys.exit(1)
    
    console.print(f"\n🎯 Starting reconnaissance on: [bold cyan]{target}[/bold cyan]")
    
    # Confirm authorization
    if not Confirm.ask("Do you have explicit written authorization to test this target?"):
        console.print("[red]❌ Testing aborted. Authorization required.[/red]")
        sys.exit(1)
    
    async def run_recon():
        results = await agent.run_reconnaissance(target)
        
        if 'error' not in results:
            console.print("\n📊 Reconnaissance Results:")
            
            # Display port scan results
            if 'port_scan' in results:
                console.print("\n🔍 Open Ports Found:")
                for host, data in results['port_scan'].items():
                    if 'protocols' in data:
                        for protocol, ports in data['protocols'].items():
                            for port, info in ports.items():
                                if info['state'] == 'open':
                                    console.print(f"  • {host}:{port}/{protocol} - {info['name']} ({info.get('product', 'Unknown')})")
            
            # Display subdomains
            if results.get('subdomains'):
                console.print(f"\n🌐 Subdomains Found: {len(results['subdomains'])}")
                for subdomain in results['subdomains'][:5]:
                    console.print(f"  • {subdomain}")
            
            # Save results if output specified
            if output:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                console.print(f"\n💾 Results saved to: {output}")
        else:
            console.print(f"[red]❌ Error: {results['error']}[/red]")
    
    asyncio.run(run_recon())

@cli.command()
@click.option('--target', '-t', required=True, help='Target URL for vulnerability scanning')
@click.option('--output', '-o', help='Output file for results')
def scan(target, output):
    """Run vulnerability scan on target"""
    agent = SecAgent()
    agent.display_banner()
    
    if not agent.check_prerequisites():
        sys.exit(1)
    
    console.print(f"\n🎯 Starting vulnerability scan on: [bold cyan]{target}[/bold cyan]")
    
    # Confirm authorization
    if not Confirm.ask("Do you have explicit written authorization to test this target?"):
        console.print("[red]❌ Testing aborted. Authorization required.[/red]")
        sys.exit(1)
    
    async def run_scan():
        results = await agent.run_vulnerability_scan(target)
        
        if 'error' not in results:
            agent.display_results_summary(results)
            
            # Save results if output specified
            if output:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                console.print(f"\n💾 Results saved to: {output}")
        else:
            console.print(f"[red]❌ Error: {results['error']}[/red]")
    
    asyncio.run(run_scan())

@cli.command()
@click.option('--company', '-c', required=True, help='Target company name')
@click.option('--domain', '-d', required=True, help='Target domain')
@click.option('--output', '-o', help='Output file for results')
def social(company, domain, output):
    """Run social engineering assessment"""
    agent = SecAgent()
    agent.display_banner()
    
    if not agent.check_prerequisites():
        sys.exit(1)
    
    console.print(f"\n🎯 Starting social engineering assessment on: [bold cyan]{company}[/bold cyan]")
    
    # Confirm authorization
    if not Confirm.ask("Do you have explicit written authorization to assess this organization?"):
        console.print("[red]❌ Assessment aborted. Authorization required.[/red]")
        sys.exit(1)
    
    async def run_social():
        results = await agent.run_social_engineering(company, domain)
        
        if 'error' not in results:
            console.print("\n📊 Social Engineering Assessment Results:")
            
            # Display email enumeration
            if results.get('email_enumeration'):
                console.print(f"\n📧 Email Addresses Found: {len(results['email_enumeration'])}")
                for email in results['email_enumeration'][:5]:
                    console.print(f"  • {email}")
            
            # Display LinkedIn info
            if results.get('linkedin_recon', {}).get('employees'):
                employees = results['linkedin_recon']['employees']
                console.print(f"\n👥 Key Employees Identified: {len(employees)}")
                for emp in employees[:3]:
                    console.print(f"  • {emp['name']} - {emp['position']}")
            
            # Save results if output specified
            if output:
                with open(output, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                console.print(f"\n💾 Results saved to: {output}")
        else:
            console.print(f"[red]❌ Error: {results['error']}[/red]")
    
    asyncio.run(run_social())

@cli.command()
@click.option('--target', '-t', required=True, help='Primary target (IP/domain)')
@click.option('--company', '-c', help='Company name for social engineering')
@click.option('--scope', '-s', multiple=True, help='Additional targets in scope')
@click.option('--output-dir', '-o', default='./reports', help='Output directory for reports')
def full(target, company, scope, output_dir):
    """Run comprehensive penetration test"""
    agent = SecAgent()
    agent.display_banner()
    
    if not agent.check_prerequisites():
        sys.exit(1)
    
    console.print(f"\n🎯 Starting comprehensive penetration test on: [bold cyan]{target}[/bold cyan]")
    
    if scope:
        console.print("📋 Additional targets in scope:")
        for s in scope:
            console.print(f"  • {s}")
    
    # Confirm authorization
    if not Confirm.ask("Do you have explicit written authorization to test all specified targets?"):
        console.print("[red]❌ Testing aborted. Authorization required.[/red]")
        sys.exit(1)
    
    async def run_full_assessment():
        console.print("\n🚀 Starting comprehensive assessment...")
        
        # Phase 1: Reconnaissance
        console.print("\n" + "="*60)
        console.print("📡 PHASE 1: RECONNAISSANCE")
        console.print("="*60)
        
        recon_results = await agent.run_reconnaissance(target)
        
        # Phase 2: Vulnerability Scanning
        console.print("\n" + "="*60)
        console.print("🔍 PHASE 2: VULNERABILITY SCANNING")
        console.print("="*60)
        
        # Use web crawl results if available
        forms = []
        if 'web_crawl' in recon_results:
            forms = recon_results['web_crawl'].get('forms', [])
        
        vuln_results = await agent.run_vulnerability_scan(f"http://{target}", forms)
        
        # Phase 3: Social Engineering (if company specified)
        if company:
            console.print("\n" + "="*60)
            console.print("👥 PHASE 3: SOCIAL ENGINEERING ASSESSMENT")
            console.print("="*60)
            
            social_results = await agent.run_social_engineering(company, target)
        
        # Phase 4: Exploitation
        console.print("\n" + "="*60)
        console.print("💥 PHASE 4: EXPLOITATION")
        console.print("="*60)
        
        exploit_results = await agent.run_exploitation(vuln_results)
        
        # Phase 5: Reporting
        console.print("\n" + "="*60)
        console.print("📊 PHASE 5: REPORT GENERATION")
        console.print("="*60)
        
        report_results = await agent.generate_report()
        
        # Display final summary
        console.print("\n" + "="*60)
        console.print("✅ ASSESSMENT COMPLETE")
        console.print("="*60)
        
        if report_results.get('html_report_path'):
            console.print(f"📄 HTML Report: {report_results['html_report_path']}")
        
        if report_results.get('json_report_path'):
            console.print(f"📄 JSON Report: {report_results['json_report_path']}")
        
        # Display vulnerability summary
        all_vulns = []
        for module_data in agent.assessment_data.values():
            if isinstance(module_data, dict) and 'vulnerabilities' in module_data:
                all_vulns.extend(module_data['vulnerabilities'])
        
        if all_vulns:
            severity_counts = {}
            for vuln in all_vulns:
                severity = vuln.get('severity', 'Medium')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            console.print(f"\n🎯 Total Vulnerabilities Found: {len(all_vulns)}")
            for severity, count in severity_counts.items():
                color = {
                    'Critical': 'red',
                    'High': 'red',
                    'Medium': 'yellow',
                    'Low': 'green'
                }.get(severity, 'white')
                console.print(f"  • {severity}: {count}", style=color)
        
        console.print("\n🛡️ Remember: Use these findings responsibly and only for authorized testing!")
    
    asyncio.run(run_full_assessment())

@cli.command()
@click.option('--payload-type', '-p', required=True, 
              type=click.Choice(['reverse_shell', 'sql_injection', 'xss', 'phishing']),
              help='Type of payload to generate')
@click.option('--target-info', '-i', help='Target information (JSON format)')
@click.option('--lhost', help='Local host for reverse shells')
@click.option('--lport', type=int, help='Local port for reverse shells')
def generate(payload_type, target_info, lhost, lport):
    """Generate payloads using AI"""
    agent = SecAgent()
    
    if not agent.check_prerequisites():
        sys.exit(1)
    
    console.print(f"\n🔧 Generating {payload_type} payload...")
    
    if payload_type == 'reverse_shell':
        if not lhost or not lport:
            console.print("[red]❌ --lhost and --lport required for reverse shells[/red]")
            sys.exit(1)
        
        payload = agent.exploit.generate_reverse_shell(lhost, lport, 'bash')
        console.print("\n🐚 Reverse Shell Payload:")
        console.print(Panel(payload, title="Bash Reverse Shell"))
        
    elif payload_type in ['sql_injection', 'xss', 'phishing']:
        if not target_info:
            target_info = "{}"
        
        try:
            target_data = json.loads(target_info)
        except json.JSONDecodeError:
            console.print("[red]❌ Invalid JSON format for target info[/red]")
            sys.exit(1)
        
        payload = agent.llm.generate_payload(payload_type, target_data)
        console.print(f"\n💉 {payload_type.title()} Payload:")
        console.print(Panel(payload, title=f"{payload_type.title()} Payload"))

if __name__ == '__main__':
    cli()
