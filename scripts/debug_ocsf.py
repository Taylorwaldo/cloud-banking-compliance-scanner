#!/usr/bin/env python3
"""Debug OCSF format to understand structure"""

import json
import sys
from pathlib import Path

def analyze_ocsf(filename):
    print(f"Analyzing: {filename}\n")
    
    # Read first few lines to understand structure
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i >= 3:  # Just check first 3 lines
                break
            if line.strip():
                try:
                    obj = json.loads(line)
                    print(f"Line {i+1} structure:")
                    print(f"  Keys: {list(obj.keys())}")
                    print(f"  status_code: {obj.get('status_code', 'NOT FOUND')}")
                    print(f"  severity_id: {obj.get('severity_id', 'NOT FOUND')}")
                    print(f"  finding_info: {obj.get('finding_info', {}).keys() if obj.get('finding_info') else 'NOT FOUND'}")
                    
                    # Check for status in different locations
                    if 'status' in obj:
                        print(f"  status: {obj.get('status')}")
                    if 'Status' in obj:
                        print(f"  Status: {obj.get('Status')}")
                    
                    # Look for check results
                    if 'finding_info' in obj:
                        finding = obj['finding_info']
                        print(f"  finding_info.title: {finding.get('title', 'NOT FOUND')[:50]}...")
                    
                    print(f"  message: {obj.get('message', '')[:100]}...")
                    print()
                    
                except json.JSONDecodeError as e:
                    print(f"Line {i+1}: Failed to parse - {e}")
    
    # Count total lines and get statistics
    passed = 0
    failed = 0
    total_lines = 0
    
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    obj = json.loads(line)
                    total_lines += 1
                    
                    # Try different status fields
                    status_code = obj.get('status_code')
                    status = obj.get('status')
                    Status = obj.get('Status')
                    
                    if status_code == 1:
                        passed += 1
                    elif status_code == 2:
                        failed += 1
                    elif status == 'PASS':
                        passed += 1
                    elif status == 'FAIL':
                        failed += 1
                    elif Status == 'PASS':
                        passed += 1
                    elif Status == 'FAIL':
                        failed += 1
                        
                except:
                    continue
    
    print(f"\nStatistics:")
    print(f"  Total lines: {total_lines}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Unknown: {total_lines - passed - failed}")

if __name__ == "__main__":
    # Find the OCSF file
    if len(sys.argv) > 1:
        analyze_ocsf(sys.argv[1])
    else:
        # Find latest OCSF file
        reports_dir = Path("reports")
        ocsf_files = list(reports_dir.glob("*.ocsf.json"))
        if ocsf_files:
            latest = max(ocsf_files, key=lambda p: p.stat().st_mtime)
            analyze_ocsf(latest)
        else:
            print("No OCSF files found")
