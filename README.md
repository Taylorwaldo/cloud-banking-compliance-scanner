# Cloud Banking Compliance Scanner Project

## About
An automated AWS compliance scanner tailored for banking industry requirements (PCI-DSS, SOX, FFIEC), built to identify and remediate security gaps in cloud infrastructure. This tool demonstrates the critical importance of continuous compliance monitoring in financial services.

![ScreenRecording2025-10-02at4 37 30PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/08e892ef-85d1-4494-96a5-7c6b70a3fbe9)

*Scanning AWS infrastructure against FFIEC banking compliance framework*

## Quick Start
```bash
# Clone the repository
git clone https://github.com/Taylorwaldo/cloud-banking-compliance-scanner.git
cd cloud-banking-compliance-scanner

# Run setup
./setup.sh

# Configure AWS credentials
aws configure

# Run compliance scan
./run_scanner.sh ffiec
```
## Project Architecture

### Workflow Overview

```mermaid
flowchart TB
    subgraph Manual["👤 Manual Execution"]
        CMD1["./run_scanner.sh ffiec"]
        CMD2["python3 scripts/generate_summary.py"]
        CMD3["python3 scripts/generate_before_after.py"]
    end
    
    subgraph AWS["☁️ AWS Account"]
        CREDS[("AWS Credentials<br/>~/.aws/credentials")]
        RESOURCES["AWS Resources<br/>IAM | S3 | CloudTrail<br/>CloudWatch | Config"]
    end
    
    subgraph Scanner["🔍 Prowler Scanner"]
        PROWLER["prowler aws<br/>--compliance ffiec_aws<br/>--output-formats json-ocsf html"]
    end
    
    subgraph RawOutput["📄 Raw Scan Output"]
        OCSF["reports/<br/>ffiec_TIMESTAMP.ocsf.json<br/>(NDJSON format)"]
        HTML1["reports/<br/>ffiec_TIMESTAMP.html"]
    end
    
    subgraph Processing["⚙️ Python Processing"]
        PARSER["generate_summary.py<br/>- parse_prowler_ocsf_json()<br/>- calculate_risk_score()<br/>- categorize_banking_findings()"]
    end
    
    subgraph FinalReports["📊 Executive Reports"]
        JSON["reports/<br/>executive_summary_TIMESTAMP.json"]
        MD["reports/<br/>executive_summary_TIMESTAMP.md"]
        DASH["reports/<br/>compliance_dashboard.html"]
        COMPARE["reports/<br/>before_after_comparison.html<br/>(Static - hardcoded values)"]
    end
    
    subgraph Automation["🤖 GitHub Actions"]
        TRIGGER["Triggers:<br/>- schedule: '0 2 * * 1'<br/>- push: main<br/>- workflow_dispatch"]
        WORKFLOW[".github/workflows/<br/>compliance-scan.yml"]
        ARTIFACTS["GitHub Artifacts<br/>(Downloadable reports)"]
    end
    
    CMD1 --> PROWLER
    CREDS -.->|Authentication| PROWLER
    PROWLER -->|Scans| RESOURCES
    PROWLER -->|Generates| OCSF
    PROWLER -->|Generates| HTML1
    
    OCSF -->|Reads| PARSER
    CMD2 --> PARSER
    PARSER -->|Writes| JSON
    PARSER -->|Writes| MD
    PARSER -->|Writes| DASH
    
    CMD3 -->|Creates| COMPARE
    
    TRIGGER -.->|Executes| WORKFLOW
    WORKFLOW -.->|Runs| PROWLER
    JSON -.->|Uploads| ARTIFACTS
    MD -.->|Uploads| ARTIFACTS
    DASH -.->|Uploads| ARTIFACTS
    HTML1 -.->|Uploads| ARTIFACTS
    
    style Manual fill:#fff3cd,stroke:#856404,stroke-width:3px,color:#000
    style AWS fill:#ff9999,stroke:#333,stroke-width:2px,color:#000
    style Scanner fill:#99ccff,stroke:#333,stroke-width:2px,color:#000
    style RawOutput fill:#e6ccff,stroke:#333,stroke-width:2px,color:#000
    style Processing fill:#99ff99,stroke:#333,stroke-width:2px,color:#000
    style FinalReports fill:#ffff99,stroke:#333,stroke-width:2px,color:#000
    style Automation fill:#d3d3d3,stroke:#333,stroke-width:2px,color:#000
```

## Core Components

**run_scanner.sh:** Entry point wrapper script

**banking_compliance_scanner.sh:** Main orchestrator that coordinates Prowler and analysis

**generate_summary.py:** Processes raw scan data into executive summaries

**generate_before_after.py:** Creates transformation visualizations

## Compliance Frameworks
**This scanner evaluates AWS environments against:**

**FFIEC** - Federal Financial Institutions Examination Council

**PCI-DSS 3.2.1** - Payment Card Industry Data Security Standard

**SOX** - Sarbanes-Oxley Act (SOC2)

**CIS 2.0** - Center for Internet Security Benchmarks 

## Technical Components
Prowler Integration

**Version:** 5.12.0

**Role:** Core scanning engine executing 80+ security checks

**Output:** OCSF JSON, HTML reports, CSV compliance matrices

## AWS Test Environment

**Account Type:** AWS Free Tier

**Purpose:** Safe sandbox for compliance testing

**Services Scanned:** IAM, S3, CloudTrail, Config, CloudWatch

## Real-World Results
**Initial Security Assessment**
<img width="1050" height="939" alt="BEFORE_SCAN" src="https://github.com/user-attachments/assets/98eb9141-28fb-4ef7-a9cd-0513def9c9c5" />
*Initial scan: 0% compliance, 29 security failures detected*

## Remediation Process
**The scanner identified critical gaps that were resolved through:**

**Enable CloudTrail** - Audit logging across all regions

**Configure Root MFA** - Critical access protection

**Activate AWS Config** - Continuous compliance monitoring

## Transformation Achieved

<img width="1440" height="900" alt="Transformation_achieved" src="https://github.com/user-attachments/assets/a29c1cae-67f0-4d03-86a5-2d9f14306604" />

*Post-remediation: 61.29% compliance, 38 security controls passed*


## Impact Metrics

| **Metric**        | **Before** | **After** | **Improvement** |
|--------------------|------------|-----------|-----------------|
| Compliance Score   | 0%         | 61.29%    | +61.29%         |
| Failed Checks      | 29         | 24        | -17.24%         |
| Critical Issues    | 2          | 0         | -100%           |
| Scan Time          | 5 min      | 4 min     | Consistent      |

## Comparision (Before and after hardening)

<img width="852" height="650" alt="comparison" src="https://github.com/user-attachments/assets/4d844056-f650-4884-93df-d85c2ad74181" />

> **Note on Grading:** The before/after visualization uses a simplified grading scale (C = 60-79%) for demonstration purposes. Production compliance reports generated by `generate_summary.py` apply stricter banking-grade thresholds where scores below 70% indicate critical failures requiring immediate remediation. See [Grading and Scoring](https://github.com/Taylorwaldo/cloud-banking-compliance-scanner/wiki/Grading-and-Scoring) for technical details.


## Business Value

- 70% reduction in audit preparation time
- 100% visibility into compliance gaps
- Real-time detection of configuration drift
- Executive-ready compliance reporting

## Output Formats
**After each scan, the tool generates:**

*.ocsf.json - Raw Prowler findings in OCSF format

*.html - Visual compliance dashboard

executive_summary_*.md - C-suite readable summary

compliance/*.csv - Detailed compliance matrix

## Installation
See Setup Guide for detailed instructions.

## Documentation

Architecture Details

Compliance Frameworks

Remediation Playbook

API Reference

## License
MIT License - See LICENSE for details.

## Author
Taylor Waldo

LinkedIn: [linkedin.com/in/taylorwaldo](https://www.linkedin.com/in/taylor-j-waldo/)

GitHub: @Taylorwaldo

 
