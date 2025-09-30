#!/bin/bash

echo "Setting up Banking Compliance Scanner..."

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment and install requirements
echo -e "${YELLOW}Installing Python requirements...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p reports configs docs tests

# Make scripts executable
chmod +x scripts/*.sh
chmod +x scripts/*.py
chmod +x tests/*.sh

# Test AWS connection
if aws sts get-caller-identity &> /dev/null; then
    echo -e "${GREEN}✓ AWS connection successful${NC}"
    aws sts get-caller-identity --output table
else
    echo -e "${RED}⚠ Please configure AWS credentials${NC}"
    echo "Run: aws configure"
fi

# Check if Prowler is available system-wide or in venv
if command -v prowler &> /dev/null; then
    echo -e "${GREEN}✓ Prowler found (system-wide)${NC}"
    prowler -v
elif venv/bin/prowler --version &> /dev/null 2>&1; then
    echo -e "${GREEN}✓ Prowler found (virtual environment)${NC}"
    venv/bin/prowler -v
else
    echo -e "${YELLOW}Installing Prowler in virtual environment...${NC}"
    pip install prowler-cloud
    echo -e "${GREEN}✓ Prowler installed${NC}"
fi

echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "To run the scanner:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: ./scripts/banking_compliance_scanner.sh"
echo ""
echo "Or run directly: ./run_scanner.sh"
echo -e "${GREEN}════════════════════════════════════════${NC}"

# Create a convenience run script
cat > run_scanner.sh << 'RUNNER'
#!/bin/bash
# Convenience script to run scanner with virtual environment

source venv/bin/activate
./scripts/banking_compliance_scanner.sh "$@"
RUNNER

chmod +x run_scanner.sh

# Deactivate virtual environment
deactivate 2>/dev/null || true
