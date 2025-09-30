#!/usr/bin/env python3
"""Parse Prowler console output to generate summary"""

import re
import json
from datetime import datetime
from pathlib import Path

def parse_prowler_results(scan_output_file=None):
    """Parse the Prowler scan results from console output or recent scan"""
    
    # If no file specified, try to get from last scan output
    if not scan_output_file:
        print("Please run: ./run_scanner.sh ffiec 2>&1 | tee scan_output.txt")
        print("Then run: python3 scripts/parse_prowler_output.py scan_output.txt")
        return
    
    with open(scan_output_file, 'r') as f:
        content = f.read()
    
    # Extract key metrics using regex
    results = {}
    
    # Find failed percentage
    failed_match = re.search(r'(\d+\.?\d*)%\s+\((\d+)\)\s+Failed', content)
    if failed_match:
        results['failed_percentage'] = float(failed_match.group(1))
        results['failed_count'] = int(failed_match.group(2))
    
    # Find passed percentage
    passed_match = re.search(r'(\d+\.?\d*)%\s+\((\d+)\)\s+Passed', content)
    if passed_match:
        results['passed_percentage'] = float(passed_match.group(1))
        results['passed_count'] = int(passed_match.group(2))
    else:
        results['passed_percentage'] = 0
        results['passed_count'] = 0
    
    # Find service breakdowns
    service_pattern = r'│\s+aws\s+│\s+(\w+)\s+│\s+FAIL \((\d+)\)\s+│\s+(\d+)\s+│\s+(\d+)\s+│\s+(\d+)\s+│\s+(\d+)'
    services = re.findall(service_pattern, content)
    
    results['services'] = {}
    results['total_critical'] = 0
    results['total_high'] = 0
    results['total_medium'] = 0
    results['total_low'] = 0
    
    for service in services:
        service_name = service[0]
        fail_count = int(service[1])
        critical = int(service[2])
        high = int(service[3])
        medium = int(service[4])
        low = int(service[5])
        
        results['services'][service_name] = {
            'failures': fail_count,
            'critical': critical,
            'high': high,
            'medium': medium,
            'low': low
        }
        
        results['total_critical'] += critical
        results['total_high'] += high
        results['total_medium'] += medium
        results['total_low'] += low
    
    # Calculate compliance score
    total = results.get('failed_count', 0) + results.get('passed_count', 0)
    if total > 0:
        results['compliance_score'] = round((results['passed_count'] / total) * 100, 2)
    else:
        results['compliance_score'] = 0
    
    # Generate grade
    score = results['compliance_score']
    if score >= 95:
        results['grade'] = 'A+ (Exceeds Banking Standards)'
    elif score >= 90:
        results['grade'] = 'A (Meets Banking Standards)'
    elif score >= 80:
        results['grade'] = 'B (Acceptable with Improvements Needed)'
    elif score >= 70:
        results['grade'] = 'C (Significant Gaps - Regulatory Risk)'
    else:
        results['grade'] = 'F (Critical - Immediate Action Required)'
    
    return results

def generate_summary_from_results(results, timestamp):
    """Generate executive summary from parsed results"""
    
    summary = f"""# Banking Compliance Executive Summary

**Date:** {datetime.now().isoformat()}
**Scan Timestamp:** {timestamp}

## Overall Compliance Score: {results['compliance_score']}%
**Grade:** {results['grade']}

## Key Metrics
- Total Checks Failed: {results.get('failed_count', 0)}
- Total Checks Passed: {results.get('passed_count', 0)}
- Critical Issues: {results['total_critical']}
- High Priority Issues: {results['total_high']}
- Medium Priority Issues: {results['total_medium']}
- Low Priority Issues: {results['total_low']}

## Service Breakdown
"""
    
    for service, details in results.get('services', {}).items():
        summary += f"\n### {service.upper()}\n"
        summary += f"- Failures: {details['failures']}\n"
        if details['critical'] > 0:
            summary += f"- **Critical: {details['critical']}** 🔴\n"
        if details['high'] > 0:
            summary += f"- **High: {details['high']}** 🟡\n"
        if details['medium'] > 0:
            summary += f"- Medium: {details['medium']}\n"
        if details['low'] > 0:
            summary += f"- Low: {details['low']}\n"
    
    # Add recommendations based on findings
    summary += "\n## Priority Recommendations\n"
    
    if results['total_critical'] > 0:
        summary += """
### 🔴 CRITICAL - Immediate Action Required (24 hours)
- Enable MFA for root account
- Review and secure IAM policies
- Document changes in compliance tracker
"""
    
    if results['total_high'] > 10:
        summary += """
### 🟡 HIGH - Fix within 1 week
- Enable CloudTrail in all regions
- Configure log file validation
- Set up centralized logging
"""
    
    if results.get('services', {}).get('config', {}).get('failures', 0) > 0:
        summary += """
### 🟠 MEDIUM - Fix within 30 days
- Enable AWS Config service
- Configure compliance rules
- Set up configuration snapshots
"""
    
    # Add compliance impact
    summary += f"""
## Compliance Impact

"""
    if results['compliance_score'] < 50:
        summary += "⚠️ **CRITICAL**: This environment has severe compliance gaps that could result in:\n"
        summary += "- Regulatory fines\n"
        summary += "- Failed audits\n"
        summary += "- Data breach risk\n"
        summary += "- Reputational damage\n"
    elif results['compliance_score'] < 80:
        summary += "⚠️ **WARNING**: Significant improvements needed to meet banking standards:\n"
        summary += "- Address all critical and high findings\n"
        summary += "- Implement logging and monitoring\n"
        summary += "- Review access controls\n"
    else:
        summary += "✅ **GOOD**: Basic compliance achieved with room for improvement:\n"
        summary += "- Continue remediation efforts\n"
        summary += "- Focus on medium priority items\n"
        summary += "- Schedule regular compliance scans\n"
    
    return summary

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Try to parse from the scan we know about
        print("\nBased on your FFIEC scan results:")
        print("-" * 50)
        
        # Manually input the results we saw
        results = {
            'failed_count': 29,
            'passed_count': 0,
            'failed_percentage': 100.0,
            'passed_percentage': 0.0,
            'compliance_score': 0.0,
            'grade': 'F (Critical - Immediate Action Required)',
            'total_critical': 2,
            'total_high': 17,
            'total_medium': 9,
            'total_low': 1,
            'services': {
                'cloudtrail': {'failures': 17, 'critical': 0, 'high': 17, 'medium': 0, 'low': 0},
                'cloudwatch': {'failures': 4, 'critical': 0, 'high': 0, 'medium': 4, 'low': 0},
                'iam': {'failures': 8, 'critical': 2, 'high': 0, 'medium': 5, 'low': 1}
            }
        }
        
        summary = generate_summary_from_results(results, '20250930_161048')
        print(summary)
        
        # Save the summary
        with open('reports/executive_summary_ffiec.md', 'w') as f:
            f.write(summary)
        print("\n✅ Summary saved to: reports/executive_summary_ffiec.md")
        
    else:
        # Parse from file
        results = parse_prowler_results(sys.argv[1])
        if results:
            summary = generate_summary_from_results(results, datetime.now().strftime('%Y%m%d_%H%M%S'))
            print(summary)
