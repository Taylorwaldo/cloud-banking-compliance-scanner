#!/bin/bash

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REPORTS_DIR="reports"

# Function to display available reports
show_reports() {
    echo -e "${GREEN}Available Reports:${NC}"
    echo ""
    
    # List HTML reports
    if ls $REPORTS_DIR/*.html 1> /dev/null 2>&1; then
        echo -e "${YELLOW}HTML Reports:${NC}"
        for file in $REPORTS_DIR/*.html; do
            echo "  • $(basename $file)"
        done
        echo ""
    fi
    
    # List Executive Summaries
    if ls $REPORTS_DIR/executive_summary_*.md 1> /dev/null 2>&1; then
        echo -e "${YELLOW}Executive Summaries:${NC}"
        for file in $REPORTS_DIR/executive_summary_*.md; do
            echo "  • $(basename $file)"
        done
        echo ""
    fi
    
    # List JSON reports
    if ls $REPORTS_DIR/*.json 1> /dev/null 2>&1; then
        echo -e "${YELLOW}JSON Reports:${NC}"
        for file in $REPORTS_DIR/*.json; do
            echo "  • $(basename $file)"
        done
    fi
}

# Function to open latest HTML report
open_latest() {
    LATEST_HTML=$(ls -t $REPORTS_DIR/*.html 2>/dev/null | head -n1)
    
    if [ -z "$LATEST_HTML" ]; then
        echo -e "${RED}No HTML reports found${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Opening latest report: $(basename $LATEST_HTML)${NC}"
    
    # Try different methods to open the file
    if command -v xdg-open &> /dev/null; then
        xdg-open "$LATEST_HTML"
    elif command -v firefox &> /dev/null; then
        firefox "$LATEST_HTML"
    elif command -v google-chrome &> /dev/null; then
        google-chrome "$LATEST_HTML"
    elif command -v open &> /dev/null; then
        open "$LATEST_HTML"
    else
        echo -e "${YELLOW}Could not find a browser to open the report${NC}"
        echo "Report location: $LATEST_HTML"
    fi
}

# Main execution
if [ "$1" == "list" ]; then
    show_reports
elif [ "$1" == "open" ]; then
    open_latest
else
    show_reports
    echo ""
    echo "Usage:"
    echo "  $0 list  - List all reports"
    echo "  $0 open  - Open latest HTML report in browser"
fi
