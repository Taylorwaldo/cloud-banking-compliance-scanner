#!/bin/bash

# Banking Compliance Scanner Demo Script
# This script demonstrates the capabilities of the scanner

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║     Cloud Banking Compliance Scanner Demo           ║"
echo "║     Designed for Financial Services Industry        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}Welcome to the Banking Compliance Scanner Demo!${NC}"
echo ""
echo "This tool helps banks and financial institutions:"
echo "• Ensure compliance with PCI-DSS, SOX, FFIEC regulations"
echo "• Identify critical security gaps in AWS infrastructure"
echo "• Generate executive-ready compliance reports"
echo "• Prioritize remediation efforts based on risk"
echo ""

read -p "Press Enter to start a quick compliance scan..."

echo -e "${YELLOW}Starting compliance scan...${NC}"
./run_scanner.sh quick-test

echo ""
echo -e "${GREEN}Scan complete! Now generating executive dashboard...${NC}"
sleep 2

# Show available reports
./scripts/view_report.sh list

echo ""
echo -e "${BLUE}Key Features Demonstrated:${NC}"
echo "✓ Automated compliance scanning using Prowler 5.12.0"
echo "✓ Banking-specific risk scoring algorithm"
echo "✓ Executive summary generation"
echo "✓ Multiple output formats (HTML, JSON, Markdown)"
echo "✓ Categorization by banking security domains"
echo ""

echo -e "${GREEN}Next Steps:${NC}"
echo "1. View HTML report: ./scripts/view_report.sh open"
echo "2. Run full PCI-DSS scan: ./run_scanner.sh pci-dss"
echo "3. Run comprehensive banking scan: ./run_scanner.sh all-banking"
echo ""

echo -e "${YELLOW}Project Benefits for Financial Institutions:${NC}"
echo "• Reduce audit preparation time by 70%"
echo "• Identify compliance gaps before regulatory audits"
echo "• Automated weekly compliance monitoring via CI/CD"
echo "• Risk-based prioritization for remediation"
