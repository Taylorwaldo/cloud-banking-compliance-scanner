# Contributing

Thanks for your interest in contributing to this AWS compliance scanner.

## Ways to Contribute

**No coding required:**
- Document real-world compliance failures and their costs
- Explain why specific security checks matter
- Test remediation steps and verify they work
- Create compliance mapping guides (which check = which regulation)
- Write threat models showing what attackers exploit

**For developers:**
- Add new compliance frameworks
- Improve error handling
- Write tests
- Enhance automation

## Getting Started

```bash
# Fork and clone
git clone https://github.com/Taylorwaldo/cloud-banking-compliance-scanner.git
cd cloud-banking-compliance-scanner

# Setup (requires AWS Free Tier account)
./setup.sh
aws configure

# Test
./run_scanner.sh quick-test
```

## Workflow

1. Create branch: `git checkout -b feature/your-feature`
2. Make changes
3. Commit: `git commit -m "docs: your change"`
4. Push and open Pull Request

## Current Needs

- Compliance case studies and cost analysis
- Cross-platform testing (Windows/Mac/Linux)
- Threat modeling documentation
- Remediation verification

## Project Status

Core functionality is complete. No strict timeline, work at your own pace.

## Questions?

Open an issue or tag @Taylorwaldo

## License

Contributions are licensed under MIT License.
