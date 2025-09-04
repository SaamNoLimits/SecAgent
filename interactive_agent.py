#!/usr/bin/env python3
"""
SecAgent - Interactive AI Pentesting Assistant

An intelligent, conversational penetration testing assistant that follows the Cyber Kill Chain
framework. Works like Windsurf/Cursor - you give natural language commands, it provides
exact terminal commands, analyzes results, and guides you through the pentesting process.

Author: SecAgent Development Team
Version: 1.0 - Interactive Mode
License: Educational Use Only

DISCLAIMER: This tool is for authorized penetration testing and educational purposes only.
Unauthorized use is strictly prohibited and may be illegal.
"""

import asyncio
import subprocess
import json
import re
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.syntax import Syntax
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Import our modules
from config import Config
from core.llm_interface import LLMInterface

console = Console()

class InteractivePentestingAssistant:
    def __init__(self):
        self.llm = LLMInterface()
        self.current_phase = "reconnaissance"
        self.target = None
        self.assessment_data = {
            'target': None,
            'reconnaissance': {},
            'weaponization': {},
            'delivery': {},
            'exploitation': {},
            'installation': {},
            'command_control': {},
            'actions_objectives': {},
            'command_history': [],
            'findings': []
        }
        
        # Cyber Kill Chain phases
        self.kill_chain_phases = [
            "reconnaissance",
            "weaponization", 
            "delivery",
            "exploitation",
            "installation",
            "command_control",
            "actions_objectives"
        ]
        
        self.phase_descriptions = {
            "reconnaissance": "🔍 Gathering information about the target",
            "weaponization": "🔧 Creating and preparing attack tools/payloads",
            "delivery": "📤 Delivering the weaponized payload to the target",
            "exploitation": "💥 Exploiting vulnerabilities to gain access",
            "installation": "⚙️ Installing persistent access mechanisms",
            "command_control": "🎮 Establishing command and control channels",
            "actions_objectives": "🎯 Achieving the final objectives"
        }
    
    def display_banner(self):
        """Display interactive assistant banner"""
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
║                     🤖 Interactive AI Pentesting Assistant                   ║
║                                                                               ║
║                        🛡️  For Authorized Testing Only  🛡️                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}🚀 How it works:{Style.RESET_ALL}
• Give me natural language commands (e.g., "scan ports on target.com")
• I'll provide exact terminal commands to execute
• Paste command results back to me for analysis
• I'll guide you through the Cyber Kill Chain framework
• Get intelligent next-step recommendations

{Fore.YELLOW}⚠️  LEGAL DISCLAIMER ⚠️{Style.RESET_ALL}
This tool is for authorized penetration testing and educational purposes only.
Ensure you have explicit written permission before testing any systems.

{Fore.BLUE}Interactive Mode | Following Cyber Kill Chain Framework{Style.RESET_ALL}
"""
        print(banner)
    
    def display_kill_chain_status(self):
        """Display current Cyber Kill Chain phase status"""
        table = Table(title="🎯 Cyber Kill Chain Progress")
        table.add_column("Phase", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Status", style="green")
        
        for i, phase in enumerate(self.kill_chain_phases):
            if phase == self.current_phase:
                status = "🔄 CURRENT"
                style = "yellow bold"
            elif i < self.kill_chain_phases.index(self.current_phase):
                status = "✅ COMPLETE"
                style = "green"
            else:
                status = "⏳ PENDING"
                style = "dim"
            
            table.add_row(
                phase.title().replace('_', ' '),
                self.phase_descriptions[phase],
                status
            )
        
        console.print(table)
    
    async def generate_command(self, user_request: str) -> dict:
        """Generate terminal command based on user request"""
        system_prompt = f"""You are an expert penetration tester providing exact terminal commands.
        
        Current Context:
        - Target: {self.target or 'Not set'}
        - Current Phase: {self.current_phase}
        - Phase Description: {self.phase_descriptions.get(self.current_phase, '')}
        
        Provide ONLY the exact terminal command(s) to execute, along with:
        1. The command itself
        2. Brief explanation of what it does
        3. Expected output format
        4. Any prerequisites or warnings
        
        Focus on tools like: nmap, nikto, gobuster, sqlmap, metasploit, burpsuite, etc.
        Always consider the current Cyber Kill Chain phase."""
        
        prompt = f"""
        User Request: "{user_request}"
        
        Provide the exact terminal command to execute this request. Format your response as JSON:
        {{
            "command": "exact command to run",
            "explanation": "what this command does",
            "expected_output": "what kind of output to expect",
            "warnings": "any important warnings or prerequisites",
            "phase_relevance": "how this relates to current kill chain phase"
        }}
        
        Make sure the command is ready to copy-paste and execute.
        """
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback if no JSON found
                return {
                    "command": "echo 'Could not parse command'",
                    "explanation": response,
                    "expected_output": "Error message",
                    "warnings": "Failed to parse LLM response",
                    "phase_relevance": "Unknown"
                }
        except Exception as e:
            return {
                "command": f"echo 'Error: {str(e)}'",
                "explanation": "Failed to generate command",
                "expected_output": "Error message",
                "warnings": str(e),
                "phase_relevance": "Error"
            }
    
    async def analyze_command_output(self, command: str, output: str) -> dict:
        """Analyze command output and suggest next steps"""
        system_prompt = f"""You are an expert penetration tester analyzing command output.
        
        Current Context:
        - Target: {self.target or 'Not set'}
        - Current Phase: {self.current_phase}
        - Phase Description: {self.phase_descriptions.get(self.current_phase, '')}
        
        Analyze the command output and provide:
        1. Key findings and insights
        2. Vulnerabilities or interesting discoveries
        3. Recommended next steps following Cyber Kill Chain
        4. Whether to advance to next phase
        5. Specific commands for next actions"""
        
        prompt = f"""
        Command Executed: {command}
        
        Command Output:
        {output[:3000]}  # Limit output to avoid token limits
        
        Analyze this output and provide insights in JSON format:
        {{
            "findings": ["list of key findings"],
            "vulnerabilities": ["any vulnerabilities discovered"],
            "next_steps": ["recommended next actions"],
            "advance_phase": true/false,
            "next_phase": "next kill chain phase if advancing",
            "recommended_commands": ["specific commands to run next"],
            "risk_level": "Low/Medium/High/Critical",
            "summary": "brief summary of results"
        }}
        """
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "findings": ["Could not parse analysis"],
                    "vulnerabilities": [],
                    "next_steps": ["Manual analysis required"],
                    "advance_phase": False,
                    "next_phase": self.current_phase,
                    "recommended_commands": [],
                    "risk_level": "Unknown",
                    "summary": response
                }
        except Exception as e:
            return {
                "findings": [f"Analysis error: {str(e)}"],
                "vulnerabilities": [],
                "next_steps": ["Retry analysis"],
                "advance_phase": False,
                "next_phase": self.current_phase,
                "recommended_commands": [],
                "risk_level": "Unknown",
                "summary": f"Error: {str(e)}"
            }
    
    def display_command_info(self, command_info: dict):
        """Display command information in a nice format"""
        console.print(Panel(
            f"[bold green]Command:[/bold green] {command_info['command']}\n\n"
            f"[bold blue]Explanation:[/bold blue] {command_info['explanation']}\n\n"
            f"[bold yellow]Expected Output:[/bold yellow] {command_info['expected_output']}\n\n"
            f"[bold red]Warnings:[/bold red] {command_info['warnings']}\n\n"
            f"[bold cyan]Phase Relevance:[/bold cyan] {command_info['phase_relevance']}",
            title="🔧 Command to Execute",
            border_style="green"
        ))
    
    def display_analysis(self, analysis: dict):
        """Display command output analysis"""
        # Findings
        if analysis['findings']:
            findings_text = "\n".join([f"• {finding}" for finding in analysis['findings']])
            console.print(Panel(findings_text, title="🔍 Key Findings", border_style="blue"))
        
        # Vulnerabilities
        if analysis['vulnerabilities']:
            vuln_text = "\n".join([f"• {vuln}" for vuln in analysis['vulnerabilities']])
            risk_color = {
                'Low': 'green',
                'Medium': 'yellow', 
                'High': 'red',
                'Critical': 'red bold'
            }.get(analysis['risk_level'], 'white')
            console.print(Panel(
                f"[{risk_color}]Risk Level: {analysis['risk_level']}[/{risk_color}]\n\n{vuln_text}",
                title="🚨 Vulnerabilities Found",
                border_style="red"
            ))
        
        # Next Steps
        if analysis['next_steps']:
            next_steps_text = "\n".join([f"• {step}" for step in analysis['next_steps']])
            console.print(Panel(next_steps_text, title="➡️ Recommended Next Steps", border_style="cyan"))
        
        # Recommended Commands
        if analysis['recommended_commands']:
            commands_text = "\n".join([f"• {cmd}" for cmd in analysis['recommended_commands']])
            console.print(Panel(commands_text, title="💻 Suggested Commands", border_style="green"))
        
        # Summary
        console.print(Panel(analysis['summary'], title="📋 Summary", border_style="white"))
    
    def save_session_data(self):
        """Save current session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"secagent_session_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.assessment_data, f, indent=2, default=str)
        
        console.print(f"💾 Session saved to: {filename}")
    
    async def interactive_session(self):
        """Main interactive session loop"""
        self.display_banner()
        
        # Check prerequisites
        if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
            console.print("[red]❌ No LLM API keys configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY[/red]")
            return
        
        # Get authorization
        console.print("\n[yellow]⚠️ AUTHORIZATION CHECK ⚠️[/yellow]")
        if not Confirm.ask("Do you have explicit written authorization to perform penetration testing?"):
            console.print("[red]❌ Testing aborted. Authorization required.[/red]")
            return
        
        # Set target
        self.target = Prompt.ask("\n🎯 Enter your target (IP/domain)")
        self.assessment_data['target'] = self.target
        
        console.print(f"\n✅ Target set: [bold cyan]{self.target}[/bold cyan]")
        console.print("\n[green]🚀 Interactive pentesting session started![/green]")
        console.print("[dim]Type 'help' for commands, 'quit' to exit, 'status' to see kill chain progress[/dim]")
        
        while True:
            try:
                # Display current phase
                console.print(f"\n[bold blue]Current Phase:[/bold blue] {self.current_phase.title().replace('_', ' ')}")
                console.print(f"[dim]{self.phase_descriptions[self.current_phase]}[/dim]")
                
                # Get user input
                user_input = Prompt.ask("\n🤖 What would you like me to help you with?")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    if Confirm.ask("Save session before exiting?"):
                        self.save_session_data()
                    console.print("👋 Goodbye! Stay ethical!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'status':
                    self.display_kill_chain_status()
                    continue
                
                elif user_input.lower() == 'save':
                    self.save_session_data()
                    continue
                
                elif user_input.lower().startswith('phase '):
                    new_phase = user_input.lower().replace('phase ', '').replace(' ', '_')
                    if new_phase in self.kill_chain_phases:
                        self.current_phase = new_phase
                        console.print(f"✅ Switched to phase: {new_phase.title().replace('_', ' ')}")
                    else:
                        console.print(f"❌ Invalid phase. Available: {', '.join(self.kill_chain_phases)}")
                    continue
                
                # Generate command based on user request
                console.print("\n🔄 Generating command...")
                command_info = await self.generate_command(user_input)
                
                # Display command information
                self.display_command_info(command_info)
                
                # Ask if user wants to execute
                if Confirm.ask("\n📋 Copy this command and execute it. Paste the output here when done?"):
                    # Get command output
                    output = Prompt.ask("\n📥 Paste the command output here", multiline=True)
                    
                    if output.strip():
                        # Store command and output
                        self.assessment_data['command_history'].append({
                            'timestamp': datetime.now().isoformat(),
                            'phase': self.current_phase,
                            'user_request': user_input,
                            'command': command_info['command'],
                            'output': output
                        })
                        
                        # Analyze output
                        console.print("\n🔍 Analyzing output...")
                        analysis = await self.analyze_command_output(command_info['command'], output)
                        
                        # Display analysis
                        self.display_analysis(analysis)
                        
                        # Store findings
                        if analysis['findings']:
                            self.assessment_data['findings'].extend(analysis['findings'])
                        
                        # Advance phase if recommended
                        if analysis['advance_phase'] and analysis['next_phase'] in self.kill_chain_phases:
                            if Confirm.ask(f"\n🎯 Advance to next phase: {analysis['next_phase'].title().replace('_', ' ')}?"):
                                self.current_phase = analysis['next_phase']
                                console.print(f"✅ Advanced to: {self.current_phase.title().replace('_', ' ')}")
                    else:
                        console.print("⚠️ No output provided, skipping analysis")
                
            except KeyboardInterrupt:
                console.print("\n\n⚠️ Session interrupted")
                if Confirm.ask("Save session before exiting?"):
                    self.save_session_data()
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {str(e)}[/red]")
    
    def display_help(self):
        """Display help information"""
        help_text = """
[bold green]🤖 SecAgent Interactive Commands:[/bold green]

[bold cyan]Natural Language Commands:[/bold cyan]
• "scan ports on target.com" - Get nmap command
• "run nikto on the web server" - Get nikto command  
• "enumerate directories" - Get gobuster/dirb command
• "test for SQL injection" - Get sqlmap command
• "generate reverse shell" - Get payload generation
• "scan for vulnerabilities" - Get vulnerability scanner command

[bold cyan]Control Commands:[/bold cyan]
• help - Show this help
• status - Show Cyber Kill Chain progress
• save - Save current session
• phase <name> - Switch to specific phase
• quit/exit - Exit the session

[bold cyan]Available Phases:[/bold cyan]
• reconnaissance - Information gathering
• weaponization - Tool/payload creation
• delivery - Payload delivery
• exploitation - Vulnerability exploitation
• installation - Persistence mechanisms
• command_control - C2 establishment
• actions_objectives - Final objectives

[bold yellow]Example Workflow:[/bold yellow]
1. "scan all ports on 192.168.1.100"
2. Execute the provided nmap command
3. Paste results back for analysis
4. Follow AI recommendations for next steps
5. Progress through kill chain phases
        """
        console.print(Panel(help_text, title="📚 Help", border_style="green"))

def main():
    """Main entry point"""
    assistant = InteractivePentestingAssistant()
    asyncio.run(assistant.interactive_session())

if __name__ == "__main__":
    main()
