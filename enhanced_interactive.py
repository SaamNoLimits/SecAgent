#!/usr/bin/env python3
"""
Enhanced SecAgent - Interactive AI Pentesting Assistant with Command Templates

This enhanced version includes pre-built command templates and improved intelligence
for following the Cyber Kill Chain framework more effectively.
"""

import asyncio
import json
import re
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import our modules
from config import Config
from core.llm_interface import LLMInterface
from utils.command_templates import CommandTemplates

console = Console()

class EnhancedInteractivePentestingAssistant:
    def __init__(self):
        self.llm = LLMInterface()
        self.templates = CommandTemplates()
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
            'findings': [],
            'vulnerabilities': []
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
        """Display enhanced banner"""
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
║                🤖 Enhanced Interactive AI Pentesting Assistant               ║
║                                                                               ║
║                        🛡️  For Authorized Testing Only  🛡️                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}🚀 Enhanced Features:{Style.RESET_ALL}
• 🎯 Natural Language Command Generation
• 📋 Pre-built Command Templates Library  
• 🔄 Intelligent Result Analysis
• 📊 Cyber Kill Chain Progress Tracking
• 💾 Session Management & Reporting
• 🔍 Smart Command Search & Suggestions

{Fore.YELLOW}⚠️  LEGAL DISCLAIMER ⚠️{Style.RESET_ALL}
This tool is for authorized penetration testing and educational purposes only.
Ensure you have explicit written permission before testing any systems.

{Fore.BLUE}Enhanced Interactive Mode | v1.0{Style.RESET_ALL}
"""
        print(banner)
    
    def display_kill_chain_status(self):
        """Display current Cyber Kill Chain phase status"""
        table = Table(title="🎯 Cyber Kill Chain Progress")
        table.add_column("Phase", style="cyan", width=20)
        table.add_column("Description", style="white", width=40)
        table.add_column("Status", style="green", width=15)
        table.add_column("Progress", style="yellow", width=10)
        
        for i, phase in enumerate(self.kill_chain_phases):
            # Calculate progress
            phase_data = self.assessment_data.get(phase, {})
            progress = "0%"
            if phase_data:
                progress = f"{min(len(phase_data) * 20, 100)}%"
            
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
                status,
                progress
            )
        
        console.print(table)
    
    def display_command_templates(self, phase: str = None):
        """Display available command templates for current or specified phase"""
        target_phase = phase or self.current_phase
        commands = self.templates.get_all_commands().get(target_phase, {})
        
        if not commands:
            console.print(f"[red]No templates available for phase: {target_phase}[/red]")
            return
        
        table = Table(title=f"📋 {target_phase.title().replace('_', ' ')} Command Templates")
        table.add_column("Command", style="cyan", width=20)
        table.add_column("Description", style="white", width=40)
        table.add_column("Example", style="green", width=40)
        
        for cmd_name, cmd_info in commands.items():
            table.add_row(
                cmd_name.replace('_', ' ').title(),
                cmd_info['description'],
                cmd_info['example']
            )
        
        console.print(table)
    
    async def generate_smart_command(self, user_request: str) -> dict:
        """Generate command using both AI and templates"""
        # First, try to find matching templates
        template_matches = self.templates.search_commands(user_request, self.current_phase)
        
        # Enhance AI prompt with template context
        template_context = ""
        if template_matches:
            template_context = f"\nAvailable templates for this request:\n"
            for match in template_matches[:3]:  # Top 3 matches
                template_context += f"- {match['name']}: {match['info']['template']}\n"
        
        system_prompt = f"""You are an expert penetration tester providing exact terminal commands.
        
        Current Context:
        - Target: {self.target or 'Not set'}
        - Current Phase: {self.current_phase}
        - Phase Description: {self.phase_descriptions.get(self.current_phase, '')}
        {template_context}
        
        Provide the most appropriate command considering:
        1. Current kill chain phase
        2. Available command templates
        3. Target information
        4. Security best practices
        
        Format response as JSON with exact command and detailed explanation."""
        
        prompt = f"""
        User Request: "{user_request}"
        
        Generate the best command for this request. Consider the current phase and available templates.
        
        Response format:
        {{
            "command": "exact command to run",
            "explanation": "detailed explanation of what this command does",
            "expected_output": "what kind of output to expect",
            "warnings": "important warnings or prerequisites",
            "phase_relevance": "how this relates to current kill chain phase",
            "template_used": "name of template if used, or 'custom' if AI-generated",
            "next_steps": ["suggested follow-up actions"]
        }}
        
        Target: {self.target}
        """
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            # Try to find JSON in response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                # Clean up the JSON string
                json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)  # Remove control characters
                return json.loads(json_str)
            else:
                # Fallback to template if AI fails
                if template_matches:
                    best_match = template_matches[0]
                    template_cmd = best_match['info']['template'].format(
                        target=self.target or '{target}',
                        url=f"http://{self.target}" if self.target else '{url}',
                        domain=self.target or '{domain}'
                    )
                    return {
                        "command": template_cmd,
                        "explanation": best_match['info']['description'],
                        "expected_output": "See command documentation",
                        "warnings": "Ensure you have authorization",
                        "phase_relevance": f"Part of {best_match['phase']} phase",
                        "template_used": best_match['name'],
                        "next_steps": ["Analyze output and proceed to next step"]
                    }
                else:
                    return {
                        "command": "echo 'Could not generate command'",
                        "explanation": "Failed to parse AI response and no templates matched",
                        "expected_output": "Error message",
                        "warnings": "Manual command generation required",
                        "phase_relevance": "Unknown",
                        "template_used": "none",
                        "next_steps": ["Try rephrasing your request"]
                    }
        except Exception as e:
            return {
                "command": f"echo 'Error: {str(e)}'",
                "explanation": "Command generation failed",
                "expected_output": "Error message",
                "warnings": str(e),
                "phase_relevance": "Error",
                "template_used": "none",
                "next_steps": ["Check your request and try again"]
            }
    
    async def analyze_command_output(self, command: str, output: str) -> dict:
        """Enhanced output analysis with vulnerability detection"""
        system_prompt = f"""You are an expert penetration tester analyzing command output.
        
        Current Context:
        - Target: {self.target or 'Not set'}
        - Current Phase: {self.current_phase}
        - Command: {command}
        
        Analyze the output for:
        1. Key findings and insights
        2. Security vulnerabilities
        3. Potential attack vectors
        4. Next recommended actions
        5. Phase advancement opportunities
        6. Risk assessment
        """
        
        prompt = f"""
        Command: {command}
        Output: {output[:2000]}  # Limit to avoid token limits
        
        Provide comprehensive analysis in JSON format:
        {{
            "findings": ["key discoveries"],
            "vulnerabilities": [
                {{
                    "type": "vulnerability type",
                    "severity": "Low/Medium/High/Critical",
                    "description": "detailed description",
                    "impact": "potential impact",
                    "remediation": "how to fix"
                }}
            ],
            "attack_vectors": ["potential attack methods"],
            "next_steps": ["recommended actions"],
            "advance_phase": true/false,
            "next_phase": "suggested next phase",
            "recommended_commands": ["specific commands for next steps"],
            "risk_level": "Overall risk assessment",
            "summary": "executive summary",
            "intelligence_value": "High/Medium/Low"
        }}
        """
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                
                # Store vulnerabilities in assessment data
                if analysis.get('vulnerabilities'):
                    self.assessment_data['vulnerabilities'].extend(analysis['vulnerabilities'])
                
                return analysis
            else:
                return self._create_fallback_analysis(output)
        except Exception as e:
            return self._create_fallback_analysis(output, str(e))
    
    def _create_fallback_analysis(self, output: str, error: str = None) -> dict:
        """Create fallback analysis when AI fails"""
        return {
            "findings": [f"Command output received ({len(output)} characters)"],
            "vulnerabilities": [],
            "attack_vectors": [],
            "next_steps": ["Manual analysis required"],
            "advance_phase": False,
            "next_phase": self.current_phase,
            "recommended_commands": [],
            "risk_level": "Unknown",
            "summary": error or "Analysis failed - manual review needed",
            "intelligence_value": "Low"
        }
    
    def display_enhanced_command_info(self, command_info: dict):
        """Display enhanced command information"""
        # Main command panel
        console.print(Panel(
            f"[bold green]Command:[/bold green] {command_info['command']}\n\n"
            f"[bold blue]Explanation:[/bold blue] {command_info['explanation']}\n\n"
            f"[bold yellow]Expected Output:[/bold yellow] {command_info['expected_output']}\n\n"
            f"[bold red]Warnings:[/bold red] {command_info['warnings']}\n\n"
            f"[bold cyan]Template Used:[/bold cyan] {command_info.get('template_used', 'AI Generated')}",
            title="🔧 Command to Execute",
            border_style="green"
        ))
        
        # Next steps panel
        if command_info.get('next_steps'):
            next_steps_text = "\n".join([f"• {step}" for step in command_info['next_steps']])
            console.print(Panel(next_steps_text, title="➡️ Suggested Next Steps", border_style="blue"))
    
    def display_enhanced_analysis(self, analysis: dict):
        """Display enhanced analysis with vulnerability details"""
        # Key findings
        if analysis['findings']:
            findings_text = "\n".join([f"• {finding}" for finding in analysis['findings']])
            console.print(Panel(findings_text, title="🔍 Key Findings", border_style="blue"))
        
        # Vulnerabilities with detailed info
        if analysis['vulnerabilities']:
            for vuln in analysis['vulnerabilities']:
                vuln_text = f"[bold]Type:[/bold] {vuln['type']}\n"
                vuln_text += f"[bold]Severity:[/bold] {vuln['severity']}\n"
                vuln_text += f"[bold]Description:[/bold] {vuln['description']}\n"
                vuln_text += f"[bold]Impact:[/bold] {vuln['impact']}\n"
                vuln_text += f"[bold]Remediation:[/bold] {vuln['remediation']}"
                
                severity_color = {
                    'Low': 'green',
                    'Medium': 'yellow',
                    'High': 'red',
                    'Critical': 'red bold'
                }.get(vuln['severity'], 'white')
                
                console.print(Panel(
                    vuln_text,
                    title=f"🚨 {vuln['type']} Vulnerability",
                    border_style=severity_color.split()[0]  # Remove 'bold' for border
                ))
        
        # Attack vectors
        if analysis['attack_vectors']:
            vectors_text = "\n".join([f"• {vector}" for vector in analysis['attack_vectors']])
            console.print(Panel(vectors_text, title="⚔️ Potential Attack Vectors", border_style="red"))
        
        # Intelligence value and summary
        intel_color = {'High': 'green', 'Medium': 'yellow', 'Low': 'red'}.get(analysis['intelligence_value'], 'white')
        console.print(Panel(
            f"[{intel_color}]Intelligence Value: {analysis['intelligence_value']}[/{intel_color}]\n\n"
            f"{analysis['summary']}",
            title="📊 Analysis Summary",
            border_style="white"
        ))
    
    def search_and_suggest_commands(self, query: str):
        """Search templates and suggest commands"""
        matches = self.templates.search_commands(query, self.current_phase)
        
        if matches:
            console.print(f"\n🔍 Found {len(matches)} matching commands:")
            
            table = Table()
            table.add_column("Command", style="cyan")
            table.add_column("Phase", style="yellow")
            table.add_column("Description", style="white")
            
            for match in matches[:5]:  # Show top 5
                table.add_row(
                    match['name'].replace('_', ' ').title(),
                    match['phase'].title(),
                    match['info']['description']
                )
            
            console.print(table)
        else:
            console.print("[yellow]No matching command templates found. I'll generate a custom command.[/yellow]")
    
    async def interactive_session(self):
        """Enhanced interactive session"""
        self.display_banner()
        
        # Check prerequisites
        if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
            console.print("[red]❌ No LLM API keys configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY[/red]")
            return
        
        # Authorization check
        console.print("\n[yellow]⚠️ AUTHORIZATION CHECK ⚠️[/yellow]")
        if not Confirm.ask("Do you have explicit written authorization to perform penetration testing?"):
            console.print("[red]❌ Testing aborted. Authorization required.[/red]")
            return
        
        # Set target
        self.target = Prompt.ask("\n🎯 Enter your target (IP/domain)")
        self.assessment_data['target'] = self.target
        
        console.print(f"\n✅ Target set: [bold cyan]{self.target}[/bold cyan]")
        console.print("\n[green]🚀 Enhanced interactive pentesting session started![/green]")
        
        # Show initial help
        self.display_help()
        
        while True:
            try:
                # Display current phase
                console.print(f"\n[bold blue]Current Phase:[/bold blue] {self.current_phase.title().replace('_', ' ')}")
                console.print(f"[dim]{self.phase_descriptions[self.current_phase]}[/dim]")
                
                # Get user input
                user_input = Prompt.ask("\n🤖 What would you like me to help you with?")
                
                # Handle special commands
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
                
                elif user_input.lower() == 'templates':
                    self.display_command_templates()
                    continue
                
                elif user_input.lower().startswith('templates '):
                    phase = user_input.lower().replace('templates ', '').replace(' ', '_')
                    self.display_command_templates(phase)
                    continue
                
                elif user_input.lower().startswith('search '):
                    query = user_input[7:]  # Remove 'search '
                    self.search_and_suggest_commands(query)
                    continue
                
                elif user_input.lower() == 'save':
                    self.save_session_data()
                    continue
                
                elif user_input.lower().startswith('phase '):
                    new_phase = user_input.lower().replace('phase ', '').replace(' ', '_')
                    if new_phase in self.kill_chain_phases:
                        self.current_phase = new_phase
                        console.print(f"✅ Switched to phase: {new_phase.title().replace('_', ' ')}")
                        self.display_command_templates()
                    else:
                        console.print(f"❌ Invalid phase. Available: {', '.join(self.kill_chain_phases)}")
                    continue
                
                # Generate smart command
                console.print("\n🔄 Generating intelligent command...")
                command_info = await self.generate_smart_command(user_input)
                
                # Display command information
                self.display_enhanced_command_info(command_info)
                
                # Ask if user wants to execute
                if Confirm.ask("\n📋 Copy this command and execute it. Paste the output here when done?"):
                    # Get command output
                    console.print("\n📥 Paste the command output here (press Ctrl+D when done):")
                    output_lines = []
                    try:
                        while True:
                            line = input()
                            output_lines.append(line)
                    except EOFError:
                        pass
                    output = "\n".join(output_lines)
                    
                    if output.strip():
                        # Store command and output
                        self.assessment_data['command_history'].append({
                            'timestamp': datetime.now().isoformat(),
                            'phase': self.current_phase,
                            'user_request': user_input,
                            'command': command_info['command'],
                            'output': output,
                            'template_used': command_info.get('template_used', 'AI Generated')
                        })
                        
                        # Analyze output
                        console.print("\n🔍 Analyzing output with enhanced intelligence...")
                        analysis = await self.analyze_command_output(command_info['command'], output)
                        
                        # Display enhanced analysis
                        self.display_enhanced_analysis(analysis)
                        
                        # Store findings
                        if analysis['findings']:
                            self.assessment_data['findings'].extend(analysis['findings'])
                        
                        # Store phase-specific data
                        phase_data = self.assessment_data[self.current_phase]
                        if not isinstance(phase_data, dict):
                            phase_data = {}
                        
                        phase_data[datetime.now().isoformat()] = {
                            'command': command_info['command'],
                            'analysis': analysis,
                            'intelligence_value': analysis.get('intelligence_value', 'Medium')
                        }
                        self.assessment_data[self.current_phase] = phase_data
                        
                        # Advance phase if recommended
                        if analysis['advance_phase'] and analysis['next_phase'] in self.kill_chain_phases:
                            if Confirm.ask(f"\n🎯 Advance to next phase: {analysis['next_phase'].title().replace('_', ' ')}?"):
                                self.current_phase = analysis['next_phase']
                                console.print(f"✅ Advanced to: {self.current_phase.title().replace('_', ' ')}")
                                self.display_command_templates()
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
        """Display enhanced help information"""
        help_text = """
[bold green]🤖 SecAgent Enhanced Interactive Commands:[/bold green]

[bold cyan]Natural Language Commands:[/bold cyan]
• "scan ports on target.com" - Get intelligent nmap command
• "run nikto on the web server" - Get nikto vulnerability scan
• "enumerate directories" - Get directory brute force command
• "test for SQL injection" - Get sqlmap testing command
• "generate reverse shell payload" - Get msfvenom command
• "check for weak passwords" - Get hydra brute force command

[bold cyan]Control Commands:[/bold cyan]
• help - Show this help
• status - Show Cyber Kill Chain progress
• templates - Show templates for current phase
• templates <phase> - Show templates for specific phase
• search <query> - Search command templates
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

[bold yellow]Enhanced Features:[/bold yellow]
• 📋 Smart template matching
• 🧠 AI-powered command generation
• 🔍 Intelligent output analysis
• 🚨 Automatic vulnerability detection
• 📊 Risk assessment and scoring
• 💾 Comprehensive session tracking
        """
        console.print(Panel(help_text, title="📚 Enhanced Help", border_style="green"))
    
    def save_session_data(self):
        """Save enhanced session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"secagent_enhanced_session_{timestamp}.json"
        
        # Add summary statistics
        self.assessment_data['session_summary'] = {
            'total_commands': len(self.assessment_data['command_history']),
            'vulnerabilities_found': len(self.assessment_data['vulnerabilities']),
            'phases_completed': [phase for phase in self.kill_chain_phases 
                               if self.assessment_data.get(phase)],
            'session_duration': 'Unknown',  # Could calculate if we stored start time
            'target': self.target,
            'final_phase': self.current_phase
        }
        
        with open(filename, 'w') as f:
            json.dump(self.assessment_data, f, indent=2, default=str)
        
        console.print(f"💾 Enhanced session saved to: {filename}")
        
        # Display session summary
        summary = self.assessment_data['session_summary']
        console.print(Panel(
            f"Commands Executed: {summary['total_commands']}\n"
            f"Vulnerabilities Found: {summary['vulnerabilities_found']}\n"
            f"Phases Completed: {len(summary['phases_completed'])}/7\n"
            f"Final Phase: {summary['final_phase'].title().replace('_', ' ')}",
            title="📊 Session Summary",
            border_style="blue"
        ))

def main():
    """Main entry point for enhanced assistant"""
    assistant = EnhancedInteractivePentestingAssistant()
    asyncio.run(assistant.interactive_session())

if __name__ == "__main__":
    main()
