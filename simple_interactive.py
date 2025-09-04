#!/usr/bin/env python3
"""
Simple SecAgent - Interactive AI Pentesting Assistant
A simplified version that fixes the JSON parsing and input issues
"""

import asyncio
import json
import re
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import our modules
from config import Config
from core.llm_interface import LLMInterface
from utils.command_templates import CommandTemplates

console = Console()

class SimplePentestingAssistant:
    def __init__(self):
        self.llm = LLMInterface()
        self.templates = CommandTemplates()
        self.current_phase = "reconnaissance"
        self.target = None
        self.session_data = {
            'target': None,
            'current_phase': 'reconnaissance',
            'command_history': [],
            'findings': []
        }
        
        self.kill_chain_phases = [
            "reconnaissance", "weaponization", "delivery", 
            "exploitation", "installation", "command_control", "actions_objectives"
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
        """Display simple banner"""
        banner = f"""
{Fore.CYAN}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    🤖 SecAgent - Interactive AI Assistant                     ║
║                                                                               ║
║                        🛡️  For Authorized Testing Only  🛡️                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.GREEN}🚀 How it works:{Style.RESET_ALL}
• Give natural language commands (e.g., "scan ports on target.com")
• Get exact terminal commands to execute
• Paste results back for AI analysis
• Follow Cyber Kill Chain framework

{Fore.YELLOW}⚠️ Only test systems you have permission to test!{Style.RESET_ALL}
"""
        print(banner)
    
    async def generate_command(self, user_request: str) -> dict:
        """Generate command with improved error handling"""
        # First check templates
        template_matches = self.templates.search_commands(user_request, self.current_phase)
        
        # Create a simple, focused prompt
        system_prompt = f"""You are a penetration testing expert. Generate exact terminal commands.
        
        Current phase: {self.current_phase}
        Target: {self.target or 'Not specified'}
        
        Respond with ONLY a JSON object in this exact format:
        {{"command": "exact command to run", "explanation": "what it does", "warnings": "any warnings"}}
        
        No other text before or after the JSON."""
        
        prompt = f"""User wants: "{user_request}"
        
        Generate the appropriate pentesting command for the current phase: {self.current_phase}
        
        Return only valid JSON in the specified format."""
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            
            # Clean the response
            response = response.strip()
            
            # Try to extract JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback to template if available
                if template_matches:
                    best_match = template_matches[0]
                    template_cmd = best_match['info']['template']
                    
                    # Simple parameter substitution
                    if self.target:
                        template_cmd = template_cmd.replace('{target}', self.target)
                        template_cmd = template_cmd.replace('{domain}', self.target)
                        template_cmd = template_cmd.replace('{url}', f"http://{self.target}")
                    
                    return {
                        "command": template_cmd,
                        "explanation": best_match['info']['description'],
                        "warnings": "Template-based command - verify parameters"
                    }
                else:
                    return {
                        "command": f"# Could not generate command for: {user_request}",
                        "explanation": "Try being more specific or use 'help' for examples",
                        "warnings": "Command generation failed"
                    }
                    
        except Exception as e:
            return {
                "command": f"# Error: {str(e)}",
                "explanation": "Command generation failed",
                "warnings": "Try rephrasing your request"
            }
    
    async def analyze_output(self, command: str, output: str) -> dict:
        """Analyze command output with simplified approach"""
        if not output.strip():
            return {
                "findings": ["No output provided"],
                "next_steps": ["Try running the command again"],
                "summary": "No analysis possible without output"
            }
        
        # Simple analysis prompt
        system_prompt = """You are analyzing pentesting command output. 
        Provide insights in simple JSON format.
        
        Respond with ONLY this JSON structure:
        {"findings": ["key finding 1", "key finding 2"], "next_steps": ["suggestion 1", "suggestion 2"], "summary": "brief summary"}"""
        
        prompt = f"""Command: {command}
        
        Output: {output[:1000]}
        
        Analyze this output and provide insights in the specified JSON format."""
        
        try:
            response = await self.llm.query_llm(prompt, system_prompt=system_prompt)
            
            # Extract JSON
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {
                    "findings": ["Analysis completed"],
                    "next_steps": ["Review output manually", "Continue to next phase"],
                    "summary": "Output received and logged"
                }
                
        except Exception as e:
            return {
                "findings": [f"Analysis error: {str(e)}"],
                "next_steps": ["Manual analysis required"],
                "summary": "Automated analysis failed"
            }
    
    def display_command_info(self, command_info: dict):
        """Display command information"""
        console.print(Panel(
            f"[bold green]Command:[/bold green] {command_info['command']}\n\n"
            f"[bold blue]Explanation:[/bold blue] {command_info['explanation']}\n\n"
            f"[bold red]Warnings:[/bold red] {command_info['warnings']}",
            title="🔧 Command to Execute",
            border_style="green"
        ))
    
    def display_analysis(self, analysis: dict):
        """Display analysis results"""
        if analysis['findings']:
            findings_text = "\n".join([f"• {finding}" for finding in analysis['findings']])
            console.print(Panel(findings_text, title="🔍 Findings", border_style="blue"))
        
        if analysis['next_steps']:
            steps_text = "\n".join([f"• {step}" for step in analysis['next_steps']])
            console.print(Panel(steps_text, title="➡️ Next Steps", border_style="cyan"))
        
        console.print(Panel(analysis['summary'], title="📋 Summary", border_style="white"))
    
    def get_multiline_input(self, prompt_text: str) -> str:
        """Get multiline input with simple approach"""
        console.print(f"\n{prompt_text}")
        console.print("[dim]Paste your output below, then press Enter twice to finish:[/dim]")
        
        lines = []
        empty_count = 0
        
        while empty_count < 2:
            try:
                line = input()
                if line.strip() == "":
                    empty_count += 1
                else:
                    empty_count = 0
                lines.append(line)
            except EOFError:
                break
        
        # Remove trailing empty lines
        while lines and lines[-1].strip() == "":
            lines.pop()
        
        return "\n".join(lines)
    
    def display_help(self):
        """Display help information"""
        help_text = """
[bold green]🤖 SecAgent Commands:[/bold green]

[bold cyan]Natural Language Examples:[/bold cyan]
• "scan ports on target.com"
• "run nikto on the web server"
• "enumerate directories"
• "test for SQL injection"
• "generate reverse shell"

[bold cyan]Control Commands:[/bold cyan]
• help - Show this help
• status - Show current phase
• phase <name> - Switch phase
• save - Save session
• quit - Exit

[bold cyan]Available Phases:[/bold cyan]
• reconnaissance, weaponization, delivery
• exploitation, installation, command_control
• actions_objectives
        """
        console.print(Panel(help_text, title="📚 Help", border_style="green"))
    
    def display_status(self):
        """Display current status"""
        table = Table(title="🎯 Current Status")
        table.add_column("Item", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Target", self.target or "Not set")
        table.add_row("Current Phase", self.current_phase.title().replace('_', ' '))
        table.add_row("Commands Executed", str(len(self.session_data['command_history'])))
        table.add_row("Findings", str(len(self.session_data['findings'])))
        
        console.print(table)
    
    def save_session(self):
        """Save session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"secagent_session_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.session_data, f, indent=2, default=str)
        
        console.print(f"💾 Session saved to: {filename}")
    
    async def interactive_session(self):
        """Main interactive session"""
        self.display_banner()
        
        # Check API keys
        if not Config.OPENAI_API_KEY and not Config.ANTHROPIC_API_KEY:
            console.print("[red]❌ No LLM API keys configured![/red]")
            console.print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file")
            return
        
        console.print("✅ API keys configured")
        
        # Authorization check
        console.print("\n[yellow]⚠️ AUTHORIZATION CHECK ⚠️[/yellow]")
        authorized = Confirm.ask("Do you have explicit written authorization to perform penetration testing?")
        if not authorized:
            console.print("[red]❌ Testing aborted. Authorization required.[/red]")
            return
        
        # Get target
        self.target = Prompt.ask("\n🎯 Enter your target (IP/domain)")
        self.session_data['target'] = self.target
        
        console.print(f"\n✅ Target set: [bold cyan]{self.target}[/bold cyan]")
        console.print(f"📍 Current phase: [bold blue]{self.current_phase.title().replace('_', ' ')}[/bold blue]")
        console.print(f"📖 {self.phase_descriptions[self.current_phase]}")
        
        console.print("\n[green]🚀 Interactive session started![/green]")
        console.print("[dim]Type 'help' for commands, 'quit' to exit[/dim]")
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask(f"\n🤖 [{self.current_phase}] What would you like to do?")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    if Confirm.ask("Save session before exiting?"):
                        self.save_session()
                    console.print("👋 Goodbye! Stay ethical!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'status':
                    self.display_status()
                    continue
                
                elif user_input.lower() == 'save':
                    self.save_session()
                    continue
                
                elif user_input.lower().startswith('phase '):
                    new_phase = user_input.lower().replace('phase ', '').replace(' ', '_')
                    if new_phase in self.kill_chain_phases:
                        self.current_phase = new_phase
                        self.session_data['current_phase'] = new_phase
                        console.print(f"✅ Switched to: {new_phase.title().replace('_', ' ')}")
                        console.print(f"📖 {self.phase_descriptions[new_phase]}")
                    else:
                        console.print(f"❌ Invalid phase. Available: {', '.join(self.kill_chain_phases)}")
                    continue
                
                # Generate command
                console.print("\n🔄 Generating command...")
                command_info = await self.generate_command(user_input)
                
                # Display command
                self.display_command_info(command_info)
                
                # Ask if user wants to execute
                if Confirm.ask("\n📋 Execute this command and provide output?"):
                    # Get command output
                    output = self.get_multiline_input("📥 Paste the command output:")
                    
                    if output.strip():
                        # Store command and output
                        self.session_data['command_history'].append({
                            'timestamp': datetime.now().isoformat(),
                            'phase': self.current_phase,
                            'user_request': user_input,
                            'command': command_info['command'],
                            'output': output
                        })
                        
                        # Analyze output
                        console.print("\n🔍 Analyzing output...")
                        analysis = await self.analyze_output(command_info['command'], output)
                        
                        # Display analysis
                        self.display_analysis(analysis)
                        
                        # Store findings
                        if analysis['findings']:
                            self.session_data['findings'].extend(analysis['findings'])
                    else:
                        console.print("⚠️ No output provided")
                
            except KeyboardInterrupt:
                console.print("\n\n⚠️ Session interrupted")
                if Confirm.ask("Save session before exiting?"):
                    self.save_session()
                break
            except Exception as e:
                console.print(f"[red]❌ Error: {str(e)}[/red]")
                console.print("[yellow]Try rephrasing your request or type 'help'[/yellow]")

def main():
    """Main entry point"""
    assistant = SimplePentestingAssistant()
    asyncio.run(assistant.interactive_session())

if __name__ == "__main__":
    main()
