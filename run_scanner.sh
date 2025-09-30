#!/bin/bash
# Convenience script to run scanner with virtual environment

source venv/bin/activate
./scripts/banking_compliance_scanner.sh "$@"
