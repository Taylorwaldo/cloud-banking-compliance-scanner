#!/bin/bash

# Test Banking Compliance Scanner

echo "Testing Banking Compliance Scanner..."

# Test 1: Check if Prowler is installed
if command -v prowler &> /dev/null; then
    echo "✓ Prowler installed"
else
    echo "✗ Prowler not found"
    exit 1
fi

# Test 2: Check AWS credentials
if aws sts get-caller-identity &> /dev/null; then
    echo "✓ AWS credentials configured"
else
    echo "✗ AWS credentials not configured"
    exit 1
fi

# Test 3: Run a quick scan with limited checks
echo "Running test scan..."
prowler aws --checks iam_root_mfa_enabled -M json -o /tmp

if [ $? -eq 0 ]; then
    echo "✓ Test scan completed"
else
    echo "✗ Test scan failed"
    exit 1
fi

echo "All tests passed!"
