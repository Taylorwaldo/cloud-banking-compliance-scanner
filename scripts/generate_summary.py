#!/usr/bin/env python3
"""
Banking Compliance Summary Generator
Processes Prowler OCSF outputs and creates executive dashboards
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import argparse

class ComplianceSummaryGenerator:
    def __init__(self, reports_dir, timestamp):
        self.reports_dir = Path(reports_dir)
        self.timestamp = timestamp
        self.severity_weights = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1,
            'informational': 0
        }
        
    def parse_prowler_ocsf_json(self, json_file):
        """Parse Prowler OCSF JSON output (NDJSON format)"""
        findings = []
        print(f"Parsing {json_file}...")
        try:
            with open(json_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        try:
                            finding = json.loads(line)
                            findings.append(finding)
                        except json.JSONDecodeError as e:
                            print(f"Skipping line {line_num}: {e}")
                            continue
        except Exception as e:
            print(f"Error parsing JSON file: {e}")
            
        print(f"Successfully parsed {len(findings)} findings")
        return findings
    
    def calculate_risk_score(self, findings):
        """Calculate risk score for banking environment"""
        passed = 0
        failed = 0
        
        for finding in findings:
            # OCSF format uses 'status_code'
            # 1 = Success (Pass), 2 = Failure (Fail)
            status = finding.get('status_code', 0) if isinstance(finding, dict) else 0
            
            if status == 1:
                passed += 1
            elif status == 2:
                failed += 1
        
        total = passed + failed
        if total == 0:
            return 100
        
        # Banking risk score (0-100, where 100 is most compliant)
        risk_score = (passed / total) * 100
        return round(risk_score, 2)
    
    def categorize_banking_findings(self, findings):
        """Categorize findings by banking domain"""
        categories = {
            'Data Protection': [],
            'Access Control': [],
            'Encryption': [],
            'Audit & Logging': [],
            'Network Security': [],
            'Incident Response': []
        }
        
        # Keyword mapping for banking categories
        keyword_map = {
            'Data Protection': ['s3', 'backup', 'snapshot', 'retention', 'database', 'rds', 'ebs', 'storage'],
            'Access Control': ['iam', 'mfa', 'password', 'access', 'role', 'user', 'group', 'policy', 'permission'],
            'Encryption': ['encrypt', 'kms', 'tls', 'ssl', 'certificate', 'crypto', 'key'],
            'Audit & Logging': ['cloudtrail', 'log', 'audit', 'monitor', 'config', 'cloudwatch', 'trail'],
            'Network Security': ['vpc', 'security', 'nacl', 'firewall', 'network', 'subnet', 'gateway', 'route'],
            'Incident Response': ['guardduty', 'alarm', 'sns', 'incident', 'detective', 'alert']
        }
        
        for finding in findings:
            if not isinstance(finding, dict):
                continue
                
            # OCSF format: status_code 2 = Failure
            if finding.get('status_code') != 2:
                continue
            
            # Extract text fields for categorization
            search_text = ""
            
            # Get check metadata
            metadata = finding.get('metadata', {})
            if metadata:
                product = metadata.get('product', {})
                if product:
                    feature = product.get('feature', {})
                    if feature:
                        search_text += feature.get('name', '').lower() + " "
            
            # Get finding info
            finding_info = finding.get('finding_info', {})
            if finding_info:
                search_text += finding_info.get('title', '').lower() + " "
                search_text += finding_info.get('desc', '').lower() + " "
            
            # Get resource info
            resources = finding.get('resources', [])
            if resources and len(resources) > 0:
                resource = resources[0]
                search_text += resource.get('type', '').lower() + " "
                search_text += resource.get('uid', '').lower() + " "
            
            # Get message
            message = finding.get('message', '')
            search_text += message.lower()
            
            # Categorize based on keywords
            categorized = False
            for category, keywords in keyword_map.items():
                if any(keyword in search_text for keyword in keywords):
                    categories[category].append(finding)
                    categorized = True
                    break
            
            # Default category if not matched
            if not categorized:
                # Try to determine based on service
                if 'cloudtrail' in search_text:
                    categories['Audit & Logging'].append(finding)
                elif 'iam' in search_text:
                    categories['Access Control'].append(finding)
                elif 'config' in search_text:
                    categories['Audit & Logging'].append(finding)
                else:
                    categories['Network Security'].append(finding)
        
        return categories
    
    def get_severity_from_ocsf(self, finding):
        """Extract severity from OCSF format"""
        # Check multiple possible locations for severity
        
        # First try severity_id
        severity_id = finding.get('severity_id', 0)
        if severity_id:
            severity_map = {
                0: 'unknown',
                1: 'informational',
                2: 'low',
                3: 'medium',
                4: 'high',
                5: 'critical',
                6: 'critical'  # Fatal
            }
            return severity_map.get(severity_id, 'unknown')
        
        # Then try severity field
        severity = finding.get('severity', '')
        if severity:
            return severity.lower()
        
        # Check finding_info
        finding_info = finding.get('finding_info', {})
        if finding_info:
            severity = finding_info.get('severity', '')
            if severity:
                return severity.lower()
        
        return 'medium'  # Default
    
    def generate_executive_summary(self, findings):
        """Create executive summary for banking leadership"""
        if not findings:
            print("No findings to process")
            return None
            
        risk_score = self.calculate_risk_score(findings)
        categories = self.categorize_banking_findings(findings)
        
        # Count findings by severity
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        failed_count = 0
        
        for finding in findings:
            if not isinstance(finding, dict):
                continue
                
            if finding.get('status_code') == 2:  # Failed
                failed_count += 1
                severity = self.get_severity_from_ocsf(finding)
                
                if severity == 'critical':
                    critical_count += 1
                elif severity == 'high':
                    high_count += 1
                elif severity == 'medium':
                    medium_count += 1
                elif severity == 'low':
                    low_count += 1
        
        summary = {
            'scan_date': datetime.now().isoformat(),
            'overall_risk_score': risk_score,
            'compliance_grade': self.get_compliance_grade(risk_score),
            'total_checks': len(findings),
            'passed_checks': len([f for f in findings if isinstance(f, dict) and f.get('status_code') == 1]),
            'failed_checks': failed_count,
            'critical_findings': critical_count,
            'high_findings': high_count,
            'medium_findings': medium_count,
            'low_findings': low_count,
            'categories': {}
        }
        
        for category, items in categories.items():
            summary['categories'][category] = {
                'count': len(items),
                'priority': 'HIGH' if len(items) > 5 else 'MEDIUM' if len(items) > 2 else 'LOW'
            }
        
        # Add banking-specific recommendations
        summary['recommendations'] = self.get_banking_recommendations(categories, risk_score)
        
        return summary
    
    def get_compliance_grade(self, score):
        """Convert score to banking compliance grade"""
        if score >= 95:
            return 'A+ (Exceeds Banking Standards)'
        elif score >= 90:
            return 'A (Meets Banking Standards)'
        elif score >= 80:
            return 'B (Acceptable with Improvements Needed)'
        elif score >= 70:
            return 'C (Significant Gaps - Regulatory Risk)'
        else:
            return 'F (Critical - Immediate Action Required)'
    
    def get_banking_recommendations(self, categories, risk_score):
        """Generate banking-specific recommendations"""
        recommendations = []
        
        if risk_score < 70:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Schedule emergency security review with CISO',
                'timeline': 'Within 24 hours'
            })
        
        if len(categories['Data Protection']) > 3:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Review data classification and encryption policies',
                'timeline': 'Within 1 week'
            })
        
        if len(categories['Access Control']) > 5:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Implement privileged access management (PAM) solution',
                'timeline': 'Within 30 days'
            })
        
        if len(categories['Audit & Logging']) > 10:
            recommendations.append({
                'priority': 'CRITICAL',
                'action': 'Enable CloudTrail and AWS Config immediately',
                'timeline': 'Within 48 hours'
            })
        
        if len(categories['Encryption']) > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Enable encryption for all data at rest and in transit',
                'timeline': 'Within 60 days'
            })
        
        return recommendations
    
    def save_summary(self, summary):
        """Save summary in multiple formats"""
        if not summary:
            print("No summary to save")
            return
            
        output_base = self.reports_dir / f"executive_summary_{self.timestamp}"
        
        # Save JSON
        with open(f"{output_base}.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save markdown for easy reading
        with open(f"{output_base}.md", 'w') as f:
            f.write(f"# Banking Compliance Executive Summary\n\n")
            f.write(f"**Date:** {summary['scan_date']}\n\n")
            f.write(f"## Overall Compliance Score: {summary['overall_risk_score']}%\n")
            f.write(f"**Grade:** {summary['compliance_grade']}\n\n")
            
            f.write(f"## Key Metrics\n")
            f.write(f"- Total Checks Run: {summary['total_checks']}\n")
            f.write(f"- Passed Checks: {summary['passed_checks']}\n")
            f.write(f"- Failed Checks: {summary['failed_checks']}\n")
            f.write(f"- Critical Issues: {summary['critical_findings']}\n")
            f.write(f"- High Priority Issues: {summary['high_findings']}\n")
            f.write(f"- Medium Priority Issues: {summary['medium_findings']}\n")
            f.write(f"- Low Priority Issues: {summary['low_findings']}\n\n")
            
            f.write(f"## Category Breakdown\n")
            for cat, data in summary['categories'].items():
                if data['count'] > 0:
                    f.write(f"- **{cat}:** {data['count']} issues ({data['priority']} priority)\n")
            
            if summary['recommendations']:
                f.write(f"\n## Priority Recommendations\n")
                for rec in summary['recommendations']:
                    f.write(f"\n### {rec['priority']} Priority\n")
                    f.write(f"- **Action:** {rec['action']}\n")
                    f.write(f"- **Timeline:** {rec['timeline']}\n")
            
            f.write(f"\n## Compliance Status\n")
            f.write(f"This environment currently has a **{summary['overall_risk_score']}% compliance score**, ")
            f.write(f"which indicates **{summary['compliance_grade']}**.\n\n")
            
            if summary['overall_risk_score'] < 50:
                f.write("⚠️ **URGENT**: This environment requires immediate attention to meet banking compliance standards.\n")
            elif summary['overall_risk_score'] < 80:
                f.write("⚠️ **WARNING**: Significant compliance gaps exist that could result in regulatory findings.\n")
            else:
                f.write("✅ **GOOD**: Environment meets basic compliance requirements with room for improvement.\n")
        
        print(f"\n✅ Executive summary saved:")
        print(f"  - JSON: {output_base}.json")
        print(f"  - Markdown: {output_base}.md")

def main():
    parser = argparse.ArgumentParser(description='Generate banking compliance summary')
    parser.add_argument('--reports-dir', required=True, help='Directory containing Prowler reports')
    parser.add_argument('--timestamp', required=True, help='Timestamp for this scan')
    
    args = parser.parse_args()
    
    # Find the latest OCSF JSON report
    reports_dir = Path(args.reports_dir)
    json_files = list(reports_dir.glob(f"*{args.timestamp}*.ocsf.json"))
    
    if not json_files:
        print(f"No OCSF JSON reports found for timestamp: {args.timestamp}")
        print(f"Looking in: {reports_dir}")
        return
    
    # Process the report
    generator = ComplianceSummaryGenerator(args.reports_dir, args.timestamp)
    
    for json_file in json_files:
        print(f"Processing: {json_file}")
        findings = generator.parse_prowler_ocsf_json(json_file)
        if findings:
            print(f"Found {len(findings)} checks")
            summary = generator.generate_executive_summary(findings)
            generator.save_summary(summary)
            break
        else:
            print(f"No findings in {json_file}")

if __name__ == "__main__":
    main()
