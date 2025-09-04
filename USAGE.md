# 🤖 SecAgent Interactive Usage Guide

This guide shows you how to use SecAgent's interactive AI pentesting assistant that works like Windsurf/Cursor.

## 🚀 Quick Start

### Option 1: Auto Setup (Recommended)
```bash
./start_interactive.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OpenAI or Anthropic API key

# Run interactive assistant
python3 enhanced_interactive.py
```

## 🎯 How It Works

SecAgent works like an AI coding assistant but for penetration testing:

1. **You give natural language commands**: "scan ports on target.com"
2. **AI provides exact terminal commands**: `nmap -sS -sV target.com`
3. **You execute and paste results back**
4. **AI analyzes results and suggests next steps**
5. **Process continues following Cyber Kill Chain**

## 💬 Example Conversation

```
🤖 What would you like me to help you with?
> scan all ports on 192.168.1.100

🔧 Command to Execute:
nmap -sS -sV -O -A -p- 192.168.1.100

📋 Copy this command and execute it. Paste the output here when done? Yes

📥 Paste the command output here:
> [You paste nmap results here]

🔍 Analyzing output with enhanced intelligence...

🔍 Key Findings:
• SSH service running on port 22 (OpenSSH 7.4)
• Web server running Apache 2.4.6 on ports 80/443
• MySQL database exposed on port 3306

🚨 Exposed Database Service Vulnerability
Severity: High
Description: MySQL service accessible from external network
Impact: Potential unauthorized database access
Remediation: Restrict MySQL access to localhost only

➡️ Recommended Next Steps:
• Test MySQL for weak credentials
• Scan web application for vulnerabilities
• Check for SSH brute force opportunities

🎯 Advance to next phase: Exploitation? Yes
```

## 🎮 Available Commands

### Natural Language Requests
- "scan ports on [target]"
- "run nikto on the web server"
- "enumerate directories on [url]"
- "test for SQL injection on [url]"
- "generate reverse shell payload"
- "brute force SSH on [target]"
- "check for weak passwords"
- "scan for vulnerabilities"

### Control Commands
- `help` - Show help information
- `status` - Display Cyber Kill Chain progress
- `templates` - Show command templates for current phase
- `templates [phase]` - Show templates for specific phase
- `search [query]` - Search command templates
- `phase [name]` - Switch to specific phase
- `save` - Save current session
- `quit` - Exit session

## 🎯 Cyber Kill Chain Phases

SecAgent follows the Cyber Kill Chain framework:

### 1. Reconnaissance 🔍
**Goal**: Gather information about the target
**Commands**: 
- Port scanning: "scan all ports"
- DNS enumeration: "enumerate DNS records"
- Subdomain discovery: "find subdomains"
- Web technology fingerprinting: "identify web technologies"

### 2. Weaponization 🔧
**Goal**: Create attack tools and payloads
**Commands**:
- Payload generation: "create reverse shell"
- Custom wordlists: "generate wordlist from website"
- Exploit preparation: "prepare exploit for [vulnerability]"

### 3. Delivery 📤
**Goal**: Deliver payloads to target
**Commands**:
- Start listeners: "start netcat listener"
- HTTP server: "start web server for payload delivery"
- Social engineering: "create phishing email"

### 4. Exploitation 💥
**Goal**: Exploit vulnerabilities
**Commands**:
- Web vulnerabilities: "test for SQL injection"
- Network services: "brute force SSH"
- Application testing: "scan with nikto"

### 5. Installation ⚙️
**Goal**: Install persistent access
**Commands**:
- Backdoor creation: "create persistent backdoor"
- Service installation: "install as system service"
- Registry persistence: "add registry persistence"

### 6. Command & Control 🎮
**Goal**: Establish communication channels
**Commands**:
- C2 setup: "start meterpreter handler"
- Tunnel creation: "create SSH tunnel"
- Session management: "manage active sessions"

### 7. Actions on Objectives 🎯
**Goal**: Achieve final objectives
**Commands**:
- Data exfiltration: "exfiltrate sensitive data"
- Privilege escalation: "escalate privileges"
- Lateral movement: "move to other systems"

## 🔍 Command Templates

SecAgent includes pre-built command templates for common tasks:

### Reconnaissance Templates
- `port_scan_basic`: Basic nmap scan
- `port_scan_full`: Comprehensive port scan
- `subdomain_enum`: Subdomain enumeration
- `dns_enum`: DNS reconnaissance
- `web_tech_scan`: Web technology fingerprinting

### Exploitation Templates
- `web_vuln_scan`: Nikto web vulnerability scan
- `dir_brute`: Directory brute forcing
- `sql_injection`: SQLmap testing
- `ssh_brute`: SSH brute force attack

### Weaponization Templates
- `msfvenom_reverse_shell`: Generate reverse shell
- `custom_wordlist`: Create custom wordlists
- `payload_encoder`: Encode payloads

## 🧠 AI Intelligence Features

### Smart Command Generation
- Analyzes your request in context of current phase
- Matches against command templates
- Generates custom commands when needed
- Considers target information and previous findings

### Intelligent Output Analysis
- Identifies key findings and insights
- Detects security vulnerabilities automatically
- Assesses risk levels and impact
- Suggests specific next steps
- Determines when to advance to next phase

### Vulnerability Detection
The AI automatically identifies:
- Open ports and services
- Outdated software versions
- Misconfigurations
- Potential attack vectors
- Security weaknesses

## 📊 Session Management

### Automatic Tracking
- All commands and outputs are logged
- Vulnerabilities are cataloged with details
- Phase progression is monitored
- Intelligence value is scored

### Session Persistence
```bash
# Sessions are automatically saved as JSON
secagent_enhanced_session_20240904_153045.json

# Contains:
{
  "target": "192.168.1.100",
  "current_phase": "exploitation",
  "command_history": [...],
  "vulnerabilities": [...],
  "findings": [...],
  "session_summary": {...}
}
```

### Export Options
- JSON format for programmatic access
- HTML reports for stakeholders
- Session resume capability

## 🎨 Example Workflows

### Basic Web Application Test
```
1. "scan ports on webapp.example.com"
2. "scan the web application for vulnerabilities"
3. "enumerate directories on the web server"
4. "test login form for SQL injection"
5. "generate exploit for discovered vulnerability"
```

### Network Penetration Test
```
1. "scan network 192.168.1.0/24"
2. "enumerate SMB shares on discovered hosts"
3. "brute force SSH on target systems"
4. "generate payload for compromised system"
5. "establish persistent access"
```

### Social Engineering Assessment
```
1. "gather email addresses for company.com"
2. "enumerate employees on LinkedIn"
3. "create spear phishing email template"
4. "generate malicious payload for email"
5. "setup listener for payload callbacks"
```

## ⚡ Pro Tips

### Getting Better Results
1. **Be specific**: "scan web ports" vs "scan all TCP ports"
2. **Provide context**: Mention previous findings
3. **Use phase-appropriate requests**: Don't ask for exploits during recon
4. **Review AI suggestions**: The AI learns from your target

### Command Optimization
1. **Check templates first**: Use `templates` to see available commands
2. **Search before asking**: Use `search [keyword]` to find relevant templates
3. **Customize parameters**: AI will adapt templates to your target
4. **Follow recommendations**: AI suggests logical next steps

### Session Management
1. **Save frequently**: Use `save` command regularly
2. **Track progress**: Check `status` to see kill chain advancement
3. **Document findings**: AI automatically tracks vulnerabilities
4. **Export reports**: Generate professional reports for stakeholders

## 🚨 Security & Legal

### Authorization Requirements
- **Always get written permission** before testing
- **Define clear scope** and rules of engagement
- **Respect rate limits** to avoid service disruption
- **Document everything** for legal compliance

### Ethical Usage
- Only test systems you own or have permission to test
- Don't cause damage or disruption
- Follow responsible disclosure for findings
- Respect privacy and data protection laws

### Best Practices
- Use isolated testing environments when possible
- Keep tools and techniques up to date
- Maintain professional conduct
- Provide constructive security recommendations

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Check your .env file
cat .env
# Ensure OPENAI_API_KEY or ANTHROPIC_API_KEY is set
```

**Command Not Found**
```bash
# Install missing tools
sudo apt update
sudo apt install nmap nikto sqlmap
```

**Permission Denied**
```bash
# Some commands need sudo
sudo nmap -sS target.com
```

**Network Issues**
```bash
# Check connectivity
ping target.com
# Verify firewall rules
```

### Getting Help
1. Use `help` command in interactive mode
2. Check command templates with `templates`
3. Search for specific commands with `search`
4. Review session logs for debugging
5. Check GitHub issues for known problems

## 🎓 Learning Resources

### Recommended Reading
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PTES Technical Guidelines](http://www.pentest-standard.org/)

### Practice Environments
- [VulnHub](https://www.vulnhub.com/)
- [HackTheBox](https://www.hackthebox.eu/)
- [TryHackMe](https://tryhackme.com/)
- [DVWA](http://www.dvwa.co.uk/)

### Tool Documentation
- [Nmap Reference](https://nmap.org/book/)
- [Metasploit Unleashed](https://www.offensive-security.com/metasploit-unleashed/)
- [OWASP ZAP User Guide](https://www.zaproxy.org/docs/)

---

**Remember: SecAgent is a powerful tool. Use it responsibly and ethically!** 🛡️
