# Cloud Banking Compliance Scanner

An automated AWS compliance scanner for banking industry requirements (PCI-DSS, SOX, FFIEC). Identifies and remediates security gaps in cloud infrastructure with continuous monitoring capabilities.

![ScreenRecording2025-10-02at4 37 30PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/08e892ef-85d1-4494-96a5-7c6b70a3fbe9)

*Scanning AWS infrastructure against FFIEC banking compliance framework*

---

## Quick Start

```bash
git clone https://github.com/Taylorwaldo/cloud-banking-compliance-scanner.git
cd cloud-banking-compliance-scanner
./setup.sh
aws configure
./run_scanner.sh ffiec
```

**Full installation guide:** [Installation Guide](../../wiki/Installation-Guide)

---

## Project Overview

### What It Does
- Scans AWS accounts against banking compliance frameworks
- Generates executive-ready reports in multiple formats
- Automates weekly compliance monitoring via GitHub Actions
- Tracks security improvements over time

### Supported Frameworks
- **FFIEC** - Federal Financial Institutions Examination Council
- **PCI-DSS 3.2.1** - Payment Card Industry Data Security Standard
- **SOX/SOC2** - Sarbanes-Oxley Act
- **CIS 2.0** - Center for Internet Security Benchmarks

**Details:** [Compliance Frameworks](../../wiki/Compliance-Frameworks)

---

## Architecture

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

**Technical deep dive:** [Architecture](../../wiki/Architecture)

---

## Real-World Results

### Initial Security Assessment

<img width="701" height="740" alt="Screenshot 2025-10-03 at 10 16 10 AM" src="https://github.com/user-attachments/assets/f0c1ece8-3a3e-41fd-b042-b59257f64bb5" />

*Initial scan: 0% compliance, 29 security failures*

### Transformation Achieved

<img width="852" height="650" alt="comparison" src="https://github.com/user-attachments/assets/d35abb89-cc03-438f-a8b2-aada54832d32" />

*Post-remediation: 61.29% compliance, 38 security controls passed*

### Impact Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Compliance Score | 0% | 61.29% | +61.29% |
| Failed Checks | 29 | 24 | -17.24% |
| Critical Issues | 2 | 0 | -100% |
| Scan Time | 5 min | 4 min | Consistent |

**Note:** The before/after visualization uses a simplified grading scale (C = 60-79%). Production reports use stricter banking-grade thresholds where scores below 70% indicate critical failures. See [Grading and Scoring](../../wiki/Grading-and-Scoring) for details.

**Remediation steps:** [Remediation Playbook](../../wiki/Remediation-Playbook)

---

## Business Value

- 70% reduction in audit preparation time
- 100% visibility into compliance gaps
- Real-time detection of configuration drift
- Executive-ready compliance reporting

---

## Usage

### Run a Scan
```bash
./run_scanner.sh ffiec          # Banking regulations
./run_scanner.sh pci-dss        # Payment card security
./run_scanner.sh quick-test     # Fast 3-check test
```

### View Reports
```bash
./scripts/view_report.sh list   # List all reports
./scripts/view_report.sh open   # Open latest HTML
```

**API documentation:** [API Reference](../../wiki/API-Reference)

---

## Output Formats

- `.ocsf.json` - Raw Prowler findings (OCSF format)
- `.html` - Visual compliance dashboard
- `executive_summary_*.md` - Executive-readable summary
- `compliance/*.csv` - Detailed compliance matrix

---

## Documentation

- [Installation Guide](../../wiki/Installation-Guide) - Setup instructions
- [Architecture](../../wiki/Architecture) - Technical implementation details
- [Compliance Frameworks](../../wiki/Compliance-Frameworks) - Framework specifications
- [Remediation Playbook](../../wiki/Remediation-Playbook) - Fix security issues (How I got from 0% to 61%)
- [Grading and Scoring](../../wiki/Grading-and-Scoring) - How scores are calculated
- [API Reference](../../wiki/API-Reference) - Script usage and parameters

---

## Tech Stack

- **Prowler 5.12.0** - AWS security scanner (80+ checks)
- **Python 3** - Report generation and data processing
- **Bash** - Orchestration and automation
- **GitHub Actions** - CI/CD automation
- **OCSF Format** - Standardized security event schema

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Author

**Taylor Waldo**  
[LinkedIn](https://www.linkedin.com/in/taylor-j-waldo/) | [GitHub](https://github.com/Taylorwaldo)
 
