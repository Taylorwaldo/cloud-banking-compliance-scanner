#!/bin/bash

# Banking Compliance Scanner
# Version: 1.1 - Updated for Prowler 5.12.0
# Purpose: Orchestrate Prowler scans for banking compliance

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
REPORTS_DIR="$PROJECT_ROOT/reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Check if we're in virtual environment, if not activate it
if [[ "$VIRTUAL_ENV" == "" ]]; then
    if [ -d "$PROJECT_ROOT/venv" ]; then
        echo -e "${YELLOW}[*] Activating virtual environment...${NC}"
        source "$PROJECT_ROOT/venv/bin/activate"
    fi
fi

# Determine Prowler path
PROWLER_CMD="prowler"
if ! command -v prowler &> /dev/null; then
    if [ -f "$PROJECT_ROOT/venv/bin/prowler" ]; then
        PROWLER_CMD="$PROJECT_ROOT/venv/bin/prowler"
    else
        echo -e "${RED}[!] Prowler not found. Run setup.sh first.${NC}"
        exit 1
    fi
fi

# Function: Display banner
show_banner() {
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════╗"
    echo "║   Cloud Banking Compliance Scanner    ║"
    echo "║         Powered by Prowler            ║"
    echo "╔════════════════════════════════════════╗"
    echo -e "${NC}"
}

# Function: Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}[*] Checking prerequisites...${NC}"
    
    # Check Prowler
    if ! $PROWLER_CMD --version &> /dev/null; then
        echo -e "${RED}[!] Prowler not working. Please run setup.sh${NC}"
        exit 1
    fi
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}[!] AWS CLI not found. Please install AWS CLI.${NC}"
        echo "Run: sudo apt install awscli"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}[!] AWS credentials not configured.${NC}"
        echo "Run: aws configure"
        exit 1
    fi
    
    echo -e "${GREEN}[✓] All prerequisites met${NC}"
}

# Function: Run compliance scan
run_compliance_scan() {
    local framework=$1
    local output_name="${framework}_${TIMESTAMP}"
    
    echo -e "${YELLOW}[*] Running ${framework} compliance scan...${NC}"
    
    case $framework in
        "pci-dss")
            $PROWLER_CMD aws \
                --compliance pci_3.2.1_aws \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "$output_name" \
                --status FAIL
            ;;
        "sox")
            $PROWLER_CMD aws \
                --compliance soc2_aws \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "$output_name" \
                --status FAIL
            ;;
        "cis")
            $PROWLER_CMD aws \
                --compliance cis_2.0_aws \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "$output_name" \
                --status FAIL
            ;;
        "ffiec")
            $PROWLER_CMD aws \
                --compliance ffiec_aws \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "$output_name" \
                --status FAIL
            ;;
        "quick-test")
            # Quick test with just a few checks
            echo -e "${YELLOW}[*] Running quick test scan (limited checks)...${NC}"
            $PROWLER_CMD aws \
                --check iam_root_mfa_enabled iam_password_policy_uppercase s3_bucket_public_access_block \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "quick_test_${TIMESTAMP}" \
                --status FAIL
            ;;
        "all-banking")
            # Run multiple compliance frameworks relevant to banking
            echo -e "${YELLOW}[*] Running comprehensive banking compliance scan...${NC}"
            
            # PCI-DSS
            echo -e "${YELLOW}Running PCI-DSS checks...${NC}"
            $PROWLER_CMD aws \
                --compliance pci_3.2.1_aws \
                --output-formats json-ocsf \
                --output-directory "$REPORTS_DIR" \
                --output-filename "banking_pci_${TIMESTAMP}" \
                --status FAIL
            
            # SOC2
            echo -e "${YELLOW}Running SOC2 checks...${NC}"
            $PROWLER_CMD aws \
                --compliance soc2_aws \
                --output-formats json-ocsf \
                --output-directory "$REPORTS_DIR" \
                --output-filename "banking_soc2_${TIMESTAMP}" \
                --status FAIL
            
            # FFIEC
            echo -e "${YELLOW}Running FFIEC checks...${NC}"
            $PROWLER_CMD aws \
                --compliance ffiec_aws \
                --output-formats json-ocsf html \
                --output-directory "$REPORTS_DIR" \
                --output-filename "banking_comprehensive_${TIMESTAMP}" \
                --status FAIL
            ;;
        *)
            echo -e "${RED}[!] Unknown framework: $framework${NC}"
            echo "Available options: pci-dss, sox, cis, ffiec, quick-test, all-banking"
            return 1
            ;;
    esac
    
    echo -e "${GREEN}[✓] ${framework} scan completed${NC}"
}

# Function: Generate summary report
generate_summary() {
    echo -e "${YELLOW}[*] Generating executive summary...${NC}"
    
    # Use Python from virtual environment if available
    PYTHON_CMD="python3"
    if [ -f "$PROJECT_ROOT/venv/bin/python3" ]; then
        PYTHON_CMD="$PROJECT_ROOT/venv/bin/python3"
    fi
    
    # Find the latest JSON report
    LATEST_JSON=$(ls -t "$REPORTS_DIR"/*"${TIMESTAMP}"*.ocsf.json 2>/dev/null | head -n1)
    
    if [ -z "$LATEST_JSON" ]; then
        echo -e "${YELLOW}[!] No JSON report found, skipping summary generation${NC}"
        return
    fi
    
    $PYTHON_CMD "$SCRIPT_DIR/generate_summary.py" \
        --reports-dir "$REPORTS_DIR" \
        --timestamp "$TIMESTAMP"
    
    echo -e "${GREEN}[✓] Summary generated${NC}"
}

# Function: List available compliance frameworks
list_frameworks() {
    echo -e "${GREEN}Available Banking-Relevant Compliance Frameworks:${NC}"
    echo "  • pci-dss    - PCI Data Security Standard v3.2.1"
    echo "  • sox        - SOC2 compliance"
    echo "  • cis        - CIS AWS Foundations Benchmark 2.0"
    echo "  • ffiec      - Federal Financial Institutions Examination Council"
    echo "  • all-banking - Run all banking compliance frameworks"
    echo "  • quick-test - Quick test with minimal checks"
    echo ""
    echo "To see all available Prowler compliance frameworks:"
    echo "  prowler aws --list-compliance"
}

# Main execution
main() {
    show_banner
    
    # Parse arguments
    FRAMEWORK=${1:-""}
    
    if [ -z "$FRAMEWORK" ]; then
        echo -e "${YELLOW}No framework specified${NC}"
        echo ""
        list_frameworks
        echo ""
        echo "Usage: $0 <framework>"
        echo "Example: $0 quick-test"
        exit 0
    fi
    
    if [ "$FRAMEWORK" == "list" ]; then
        list_frameworks
        exit 0
    fi
    
    check_prerequisites
    
    echo -e "${YELLOW}[*] Running framework: ${FRAMEWORK}${NC}"
    
    # Create reports directory if it doesn't exist
    mkdir -p "$REPORTS_DIR"
    
    # Run scan
    run_compliance_scan "$FRAMEWORK"
    
    # Generate summary
    generate_summary
    
    echo -e "${GREEN}"
    echo "════════════════════════════════════════"
    echo "    Scan Complete!"
    echo "    Reports saved in: $REPORTS_DIR"
    echo "    Timestamp: $TIMESTAMP"
    
    # List generated files
    echo ""
    echo "    Generated files:"
    for file in "$REPORTS_DIR"/*"$TIMESTAMP"*; do
        if [ -f "$file" ]; then
            echo "    • $(basename "$file")"
        fi
    done
    
    echo "════════════════════════════════════════"
    echo -e "${NC}"
}

# Run main function
main "$@"
