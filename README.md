# 🛡️ SecAgent - AI-Powered Red Team Penetration Testing Assistant

SecAgent is a comprehensive, AI-enhanced penetration testing framework that leverages Large Language Models (LLMs) to automate and enhance security assessments. It combines traditional security testing techniques with cutting-edge AI capabilities to provide intelligent vulnerability analysis, exploit generation, and comprehensive reporting.

## ⚠️ LEGAL DISCLAIMER

**This tool is designed for authorized penetration testing and educational purposes only.**

- You must have explicit written permission before testing any systems
- Unauthorized use is strictly prohibited and may violate local and international laws
- Users are solely responsible for ensuring compliance with applicable laws and regulations
- The developers assume no liability for misuse of this tool

## 🚀 Features

### 🔍 AI-Enhanced Reconnaissance
- Automated port scanning with intelligent analysis
- Subdomain enumeration and DNS analysis
- Web application crawling and technology detection
- WHOIS and domain intelligence gathering
- LLM-powered analysis of reconnaissance results

### 🎯 Intelligent Vulnerability Scanning
- SQL injection detection and analysis
- Cross-Site Scripting (XSS) vulnerability testing
- Directory traversal and path manipulation testing
- Command injection vulnerability assessment
- Weak authentication mechanism detection
- AI-powered vulnerability prioritization

### 💥 Automated Exploitation
- Dynamic payload generation using LLMs
- Reverse shell payload creation
- SQL injection exploitation automation
- Web shell upload attempts
- Privilege escalation techniques
- Network pivoting capabilities

### 👥 Social Engineering Assessment
- Email enumeration and OSINT gathering
- LinkedIn and social media reconnaissance
- Spear phishing template generation
- Voice phishing (vishing) script creation
- Password policy analysis and wordlist generation
- Physical security assessment

### 📊 Comprehensive Reporting
- Executive summary generation
- Technical vulnerability details
- Risk assessment and scoring
- Remediation timeline and recommendations
- Multiple output formats (HTML, JSON, PDF)
- LLM-powered report analysis and insights

### 🤖 Multi-LLM Support
- OpenAI GPT-4 integration
- Anthropic Claude integration
- Intelligent model selection based on task
- Fallback mechanisms for API failures

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/secagent.git
cd secagent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration file
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

### Required API Keys

You need at least one LLM API key:

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Anthropic API Key**: Get from [Anthropic Console](https://console.anthropic.com/)

Optional but recommended:
- **Shodan API Key**: For enhanced reconnaissance
- **Censys API Keys**: For internet-wide scanning data

## 🎮 Usage

### Command Line Interface

SecAgent provides a comprehensive CLI with multiple commands:

```bash
# Display help
python secagent.py --help

# Show banner and information
python secagent.py banner

# Run reconnaissance only
python secagent.py recon -t example.com

# Run vulnerability scan
python secagent.py scan -t http://example.com

# Run social engineering assessment
python secagent.py social -c "Example Corp" -d example.com

# Run comprehensive penetration test
python secagent.py full -t example.com -c "Example Corp"

# Generate specific payloads
python secagent.py generate -p reverse_shell --lhost 192.168.1.100 --lport 4444
python secagent.py generate -p sql_injection -i '{"database": "mysql", "parameter": "id"}'
```

### Example Workflows

#### 1. Basic Reconnaissance
```bash
python secagent.py recon -t target.com -o recon_results.json
```

#### 2. Web Application Security Assessment
```bash
python secagent.py scan -t https://webapp.example.com -o vuln_results.json
```

#### 3. Comprehensive Red Team Assessment
```bash
python secagent.py full -t company.com -c "Target Company" -s subdomain1.company.com -s subdomain2.company.com
```

#### 4. Social Engineering Campaign
```bash
python secagent.py social -c "Target Organization" -d target.org -o social_assessment.json
```

## 📁 Project Structure

```
SecAgent/
├── secagent.py              # Main CLI application
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example            # Environment configuration template
├── README.md               # This file
├── core/
│   └── llm_interface.py    # LLM integration and management
├── modules/
│   ├── reconnaissance.py   # OSINT and reconnaissance
│   ├── vulnerability_scanner.py  # Vulnerability detection
│   ├── exploitation.py     # Exploitation and payload generation
│   ├── social_engineering.py     # Social engineering assessment
│   └── reporting.py        # Report generation and analysis
├── output/                 # Scan results and temporary files
├── reports/                # Generated reports
└── logs/                   # Application logs
```

## 🔧 Configuration

### Environment Variables

Edit the `.env` file to configure SecAgent:

```bash
# Required: At least one LLM API key
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# Optional: Security intelligence APIs
SHODAN_API_KEY=your-shodan-key-here
CENSYS_API_ID=your-censys-id-here
CENSYS_API_SECRET=your-censys-secret-here

# Optional: Advanced settings
MAX_CONCURRENT_SCANS=10
REQUEST_TIMEOUT=30
LOG_LEVEL=INFO
```

### Customization

You can customize SecAgent by modifying:

- `config.py`: Default settings and wordlists
- Module files: Add new scanning techniques or modify existing ones
- Report templates: Customize report generation in `modules/reporting.py`

## 🛡️ Security Best Practices

### For Penetration Testers

1. **Always obtain written authorization** before testing
2. **Define clear scope** and rules of engagement
3. **Use rate limiting** to avoid disrupting services
4. **Document everything** for comprehensive reporting
5. **Follow responsible disclosure** for any findings

### For Organizations

1. **Regular assessments**: Use SecAgent for periodic security testing
2. **Staff training**: Use social engineering modules for awareness training
3. **Patch management**: Follow remediation timelines in reports
4. **Incident response**: Use findings to improve security procedures

## 📊 Sample Reports

SecAgent generates comprehensive reports including:

- **Executive Summary**: Business-focused risk assessment
- **Technical Details**: Detailed vulnerability analysis
- **Remediation Timeline**: Prioritized action items
- **Compliance Mapping**: Alignment with security frameworks
- **Appendices**: Raw data and proof-of-concept code

## 🤝 Contributing

We welcome contributions to SecAgent! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black secagent.py modules/ core/

# Linting
flake8 secagent.py modules/ core/
```

## 📚 Educational Resources

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)
- [OSSTMM](https://www.isecom.org/OSSTMM.3.pdf)

## 🆘 Support

If you encounter issues or have questions:

1. Check the [documentation](docs/)
2. Search [existing issues](https://github.com/your-repo/secagent/issues)
3. Create a [new issue](https://github.com/your-repo/secagent/issues/new)
4. Join our [Discord community](https://discord.gg/secagent)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI and Anthropic for LLM APIs
- The cybersecurity community for tools and techniques
- OWASP for security testing methodologies
- All contributors and testers

## 🔮 Roadmap

### Version 1.1
- [ ] Advanced evasion techniques
- [ ] Machine learning-based anomaly detection
- [ ] Integration with popular security tools
- [ ] Mobile application testing capabilities

### Version 1.2
- [ ] Cloud security assessment modules
- [ ] API security testing framework
- [ ] Automated report delivery
- [ ] Multi-target campaign management

### Version 2.0
- [ ] GUI interface
- [ ] Distributed scanning capabilities
- [ ] Advanced AI models integration
- [ ] Real-time collaboration features

---

**Remember: With great power comes great responsibility. Use SecAgent ethically and legally!** 🛡️
