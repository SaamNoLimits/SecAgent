"""
Reporting Module - Generate comprehensive penetration testing reports
"""
import json
import datetime
from typing import Dict, List, Optional
from pathlib import Path
import base64
from core.llm_interface import LLMInterface
from config import Config

class ReportingModule:
    def __init__(self):
        self.llm = LLMInterface()
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure output directories exist"""
        Path(Config.OUTPUT_DIR).mkdir(exist_ok=True)
        Path(Config.REPORTS_DIR).mkdir(exist_ok=True)
        Path(Config.LOGS_DIR).mkdir(exist_ok=True)
    
    def generate_executive_summary(self, assessment_results: Dict) -> str:
        """Generate executive summary using LLM"""
        system_prompt = """You are a senior cybersecurity consultant writing an executive summary 
        for a penetration testing report. Focus on business impact, risk assessment, and high-level recommendations."""
        
        prompt = f"""
        Create an executive summary for a penetration testing assessment with the following results:
        
        Assessment Results: {json.dumps(assessment_results, indent=2, default=str)[:2000]}
        
        Requirements:
        1. Business-focused language suitable for executives
        2. Clear risk assessment with severity levels
        3. High-level recommendations prioritized by business impact
        4. Compliance and regulatory considerations
        5. Timeline for remediation activities
        6. Budget considerations for security improvements
        
        Keep it concise but comprehensive, focusing on actionable insights.
        """
        
        return self.llm.query_llm(prompt, system_prompt=system_prompt)
    
    def generate_technical_details(self, vulnerability_results: Dict) -> str:
        """Generate detailed technical analysis"""
        system_prompt = """You are a technical security analyst providing detailed vulnerability 
        analysis for IT teams. Include technical details, proof of concept, and specific remediation steps."""
        
        prompt = f"""
        Create detailed technical analysis for the following vulnerabilities:
        
        Vulnerability Results: {json.dumps(vulnerability_results, indent=2, default=str)[:3000]}
        
        Requirements:
        1. Technical description of each vulnerability
        2. Proof of concept or evidence
        3. CVSS scoring where applicable
        4. Step-by-step remediation instructions
        5. Testing procedures to verify fixes
        6. References to security standards and best practices
        
        Provide actionable technical guidance for the IT security team.
        """
        
        return self.llm.query_llm(prompt, system_prompt=system_prompt)
    
    def calculate_risk_score(self, vulnerabilities: List[Dict]) -> Dict:
        """Calculate overall risk score based on vulnerabilities"""
        risk_weights = {
            'Critical': 10,
            'High': 7,
            'Medium': 4,
            'Low': 1,
            'Info': 0.5
        }
        
        severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Info': 0}
        total_score = 0
        
        for vuln in vulnerabilities:
            severity = vuln.get('severity', 'Medium')
            if severity in severity_counts:
                severity_counts[severity] += 1
                total_score += risk_weights[severity]
        
        # Calculate risk level
        if total_score >= 50:
            risk_level = 'Critical'
        elif total_score >= 30:
            risk_level = 'High'
        elif total_score >= 15:
            risk_level = 'Medium'
        elif total_score >= 5:
            risk_level = 'Low'
        else:
            risk_level = 'Minimal'
        
        return {
            'total_score': total_score,
            'risk_level': risk_level,
            'severity_breakdown': severity_counts,
            'total_vulnerabilities': len(vulnerabilities)
        }
    
    def generate_remediation_timeline(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """Generate remediation timeline based on severity"""
        timeline = []
        
        # Group by severity
        critical_vulns = [v for v in vulnerabilities if v.get('severity') == 'Critical']
        high_vulns = [v for v in vulnerabilities if v.get('severity') == 'High']
        medium_vulns = [v for v in vulnerabilities if v.get('severity') == 'Medium']
        low_vulns = [v for v in vulnerabilities if v.get('severity') == 'Low']
        
        if critical_vulns:
            timeline.append({
                'phase': 'Immediate (0-7 days)',
                'priority': 'Critical',
                'vulnerabilities': len(critical_vulns),
                'actions': [
                    'Address all critical vulnerabilities immediately',
                    'Implement emergency patches',
                    'Consider taking affected systems offline if necessary',
                    'Notify stakeholders and incident response team'
                ]
            })
        
        if high_vulns:
            timeline.append({
                'phase': 'Short-term (1-4 weeks)',
                'priority': 'High',
                'vulnerabilities': len(high_vulns),
                'actions': [
                    'Patch high-severity vulnerabilities',
                    'Implement additional security controls',
                    'Update security policies and procedures',
                    'Conduct security awareness training'
                ]
            })
        
        if medium_vulns:
            timeline.append({
                'phase': 'Medium-term (1-3 months)',
                'priority': 'Medium',
                'vulnerabilities': len(medium_vulns),
                'actions': [
                    'Address medium-severity vulnerabilities',
                    'Implement defense-in-depth strategies',
                    'Review and update security architecture',
                    'Enhance monitoring and detection capabilities'
                ]
            })
        
        if low_vulns:
            timeline.append({
                'phase': 'Long-term (3-6 months)',
                'priority': 'Low',
                'vulnerabilities': len(low_vulns),
                'actions': [
                    'Address remaining low-severity issues',
                    'Implement security best practices',
                    'Conduct regular security assessments',
                    'Maintain security hygiene'
                ]
            })
        
        return timeline
    
    def generate_html_report(self, assessment_data: Dict) -> str:
        """Generate comprehensive HTML report"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate risk metrics
        all_vulnerabilities = []
        for module_results in assessment_data.values():
            if isinstance(module_results, dict) and 'vulnerabilities' in module_results:
                all_vulnerabilities.extend(module_results['vulnerabilities'])
        
        risk_assessment = self.calculate_risk_score(all_vulnerabilities)
        remediation_timeline = self.generate_remediation_timeline(all_vulnerabilities)
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SecAgent Penetration Testing Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; margin-bottom: 30px; }}
                .header h1 {{ color: #2c3e50; margin: 0; font-size: 2.5em; }}
                .header p {{ color: #7f8c8d; font-size: 1.2em; margin: 10px 0; }}
                .section {{ margin: 30px 0; }}
                .section h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 15px; }}
                .risk-critical {{ background-color: #e74c3c; color: white; }}
                .risk-high {{ background-color: #e67e22; color: white; }}
                .risk-medium {{ background-color: #f39c12; color: white; }}
                .risk-low {{ background-color: #27ae60; color: white; }}
                .risk-minimal {{ background-color: #95a5a6; color: white; }}
                .risk-box {{ padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; }}
                .vuln-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .vuln-table th, .vuln-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                .vuln-table th {{ background-color: #34495e; color: white; }}
                .severity-critical {{ background-color: #e74c3c; color: white; font-weight: bold; }}
                .severity-high {{ background-color: #e67e22; color: white; font-weight: bold; }}
                .severity-medium {{ background-color: #f39c12; color: white; font-weight: bold; }}
                .severity-low {{ background-color: #27ae60; color: white; font-weight: bold; }}
                .timeline {{ background-color: #ecf0f1; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .timeline-item {{ margin: 15px 0; padding: 15px; background-color: white; border-radius: 5px; }}
                .code-block {{ background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; font-family: monospace; overflow-x: auto; }}
                .recommendation {{ background-color: #d5dbdb; padding: 15px; border-left: 5px solid #3498db; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛡️ SecAgent Penetration Testing Report</h1>
                    <p>Comprehensive Security Assessment</p>
                    <p><strong>Generated:</strong> {timestamp}</p>
                    <p><strong>Target:</strong> {assessment_data.get('target', 'Multiple Targets')}</p>
                </div>
                
                <div class="section">
                    <h2>📊 Executive Summary</h2>
                    <div class="risk-box risk-{risk_assessment['risk_level'].lower()}">
                        <h3>Overall Risk Level: {risk_assessment['risk_level'].upper()}</h3>
                        <p>Risk Score: {risk_assessment['total_score']}/100</p>
                        <p>Total Vulnerabilities Found: {risk_assessment['total_vulnerabilities']}</p>
                    </div>
                    
                    <h3>Vulnerability Breakdown</h3>
                    <table class="vuln-table">
                        <tr>
                            <th>Severity</th>
                            <th>Count</th>
                            <th>Percentage</th>
                        </tr>
        """
        
        # Add vulnerability breakdown
        total_vulns = risk_assessment['total_vulnerabilities']
        for severity, count in risk_assessment['severity_breakdown'].items():
            if count > 0:
                percentage = (count / total_vulns * 100) if total_vulns > 0 else 0
                html_template += f"""
                        <tr>
                            <td class="severity-{severity.lower()}">{severity}</td>
                            <td>{count}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
                """
        
        html_template += """
                    </table>
                </div>
                
                <div class="section">
                    <h2>🎯 Detailed Findings</h2>
        """
        
        # Add detailed vulnerability findings
        for i, vuln in enumerate(all_vulnerabilities[:10]):  # Limit to top 10 for readability
            severity_class = vuln.get('severity', 'Medium').lower()
            html_template += f"""
                    <div class="timeline-item">
                        <h4>#{i+1} {vuln.get('type', 'Unknown Vulnerability')}</h4>
                        <p><strong>Severity:</strong> <span class="severity-{severity_class}">{vuln.get('severity', 'Medium')}</span></p>
                        <p><strong>URL/Target:</strong> {vuln.get('url', vuln.get('target', 'N/A'))}</p>
                        <p><strong>Evidence:</strong> {vuln.get('evidence', 'N/A')}</p>
                        {f'<div class="code-block">{vuln.get("payload", "")}</div>' if vuln.get('payload') else ''}
                    </div>
            """
        
        # Add remediation timeline
        html_template += """
                </div>
                
                <div class="section">
                    <h2>⏰ Remediation Timeline</h2>
                    <div class="timeline">
        """
        
        for phase in remediation_timeline:
            html_template += f"""
                        <div class="timeline-item">
                            <h4>{phase['phase']} - {phase['priority']} Priority</h4>
                            <p><strong>Vulnerabilities to Address:</strong> {phase['vulnerabilities']}</p>
                            <ul>
            """
            for action in phase['actions']:
                html_template += f"<li>{action}</li>"
            
            html_template += """
                            </ul>
                        </div>
            """
        
        # Add recommendations section
        html_template += f"""
                    </div>
                </div>
                
                <div class="section">
                    <h2>💡 Recommendations</h2>
                    <div class="recommendation">
                        <h4>Immediate Actions Required:</h4>
                        <ul>
                            <li>Patch all critical and high-severity vulnerabilities immediately</li>
                            <li>Implement multi-factor authentication where missing</li>
                            <li>Review and update security policies</li>
                            <li>Conduct security awareness training for all staff</li>
                        </ul>
                    </div>
                    
                    <div class="recommendation">
                        <h4>Long-term Security Improvements:</h4>
                        <ul>
                            <li>Implement regular vulnerability scanning</li>
                            <li>Establish incident response procedures</li>
                            <li>Deploy advanced threat detection systems</li>
                            <li>Conduct annual penetration testing</li>
                        </ul>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 Technical Details</h2>
                    <p>For detailed technical information, remediation steps, and proof-of-concept code, 
                    please refer to the accompanying technical appendix.</p>
                </div>
                
                <div class="section">
                    <h2>⚖️ Legal Disclaimer</h2>
                    <p><strong>IMPORTANT:</strong> This penetration testing report was generated by SecAgent 
                    for authorized security testing purposes only. All testing was conducted with proper 
                    authorization and within the scope of the agreed-upon rules of engagement.</p>
                    
                    <p>The vulnerabilities and techniques described in this report should only be used 
                    for legitimate security testing, research, and defensive purposes. Unauthorized use 
                    of this information for malicious purposes is strictly prohibited and may be illegal.</p>
                </div>
                
                <div class="header" style="margin-top: 50px; border-top: 3px solid #2c3e50; border-bottom: none;">
                    <p style="color: #7f8c8d;">Report generated by SecAgent - AI-Powered Penetration Testing Assistant</p>
                    <p style="color: #7f8c8d; font-size: 0.9em;">For questions or clarifications, please contact your security team.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def save_report(self, report_content: str, filename: str = None) -> str:
        """Save report to file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"secagent_report_{timestamp}.html"
        
        filepath = Path(Config.REPORTS_DIR) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(filepath)
    
    def generate_json_report(self, assessment_data: Dict) -> str:
        """Generate machine-readable JSON report"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Calculate risk metrics
        all_vulnerabilities = []
        for module_results in assessment_data.values():
            if isinstance(module_results, dict) and 'vulnerabilities' in module_results:
                all_vulnerabilities.extend(module_results['vulnerabilities'])
        
        risk_assessment = self.calculate_risk_score(all_vulnerabilities)
        
        json_report = {
            'report_metadata': {
                'generated_by': 'SecAgent',
                'timestamp': timestamp,
                'version': '1.0',
                'target': assessment_data.get('target', 'Multiple Targets')
            },
            'risk_assessment': risk_assessment,
            'vulnerabilities': all_vulnerabilities,
            'remediation_timeline': self.generate_remediation_timeline(all_vulnerabilities),
            'raw_assessment_data': assessment_data
        }
        
        return json.dumps(json_report, indent=2, default=str)
    
    async def generate_comprehensive_report(self, assessment_data: Dict) -> Dict:
        """Generate comprehensive report in multiple formats"""
        print("[+] Generating comprehensive security report...")
        
        # Generate executive summary using LLM
        exec_summary = await self.llm.query_llm(
            f"Generate an executive summary for this security assessment: {json.dumps(assessment_data, default=str)[:1000]}",
            system_prompt="You are a senior cybersecurity consultant writing for executives."
        )
        
        # Generate technical details using LLM
        tech_details = await self.llm.query_llm(
            f"Generate detailed technical analysis for these vulnerabilities: {json.dumps(assessment_data, default=str)[:2000]}",
            system_prompt="You are a technical security analyst providing detailed vulnerability analysis."
        )
        
        # Generate HTML report
        html_report = self.generate_html_report(assessment_data)
        html_file = self.save_report(html_report)
        
        # Generate JSON report
        json_report = self.generate_json_report(assessment_data)
        json_file = self.save_report(json_report, filename=f"secagent_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        return {
            'executive_summary': exec_summary,
            'technical_details': tech_details,
            'html_report_path': html_file,
            'json_report_path': json_file,
            'report_generated': True
        }
