#!/usr/bin/env python3
"""Generate HTML dashboard for banking compliance"""

import json
from pathlib import Path
from datetime import datetime

def generate_html_dashboard(summary_file):
    """Create a simple HTML dashboard"""
    
    with open(summary_file, 'r') as f:
        data = json.load(f)
    
    score = data['overall_risk_score']
    color = 'green' if score >= 90 else 'yellow' if score >= 70 else 'red'
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Banking Compliance Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            .score {{ font-size: 48px; color: {color}; }}
            .grade {{ font-size: 24px; margin: 20px 0; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .critical {{ background-color: #ffcccc; }}
            .high {{ background-color: #ffe6cc; }}
            .medium {{ background-color: #ffffcc; }}
            .low {{ background-color: #ccffcc; }}
        </style>
    </head>
    <body>
        <h1>Banking Compliance Dashboard</h1>
        <div class="score">Score: {score}%</div>
        <div class="grade">Grade: {data['compliance_grade']}</div>
        
        <h2>Findings by Category</h2>
        <table>
            <tr>
                <th>Category</th>
                <th>Count</th>
                <th>Priority</th>
            </tr>
    """
    
    for cat, info in data['categories'].items():
        priority_class = info['priority'].lower()
        html += f"""
            <tr class="{priority_class}">
                <td>{cat}</td>
                <td>{info['count']}</td>
                <td>{info['priority']}</td>
            </tr>
        """
    
    html += """
        </table>
        
        <h2>Key Metrics</h2>
        <ul>
            <li>Total Findings: """ + str(data['total_findings']) + """</li>
            <li>Critical Issues: """ + str(data['critical_findings']) + """</li>
        </ul>
        
        <p><i>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</i></p>
    </body>
    </html>
    """
    
    output_file = summary_file.parent / "dashboard.html"
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"Dashboard saved to {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        generate_html_dashboard(Path(sys.argv[1]))
    else:
        print("Usage: python generate_dashboard.py <summary.json>")
