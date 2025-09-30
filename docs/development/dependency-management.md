# Dependency Management Policy

## Overview

Meta-Repo Seed uses **pinned dependency versions** for reproducible builds and security compliance, supporting the Business-in-a-Box mission of reliable, professional infrastructure.

## Dependency Structure

### 📁 **requirements.txt** (Runtime Dependencies)
**Purpose**: Core dependencies needed for production use
**Contents**: Minimal dependencies for `seeding.py` functionality
**Usage**: `pip install -r requirements.txt`

```txt
PyYAML==6.0.2      # Configuration file support
jsonschema==4.25.1 # JSON Schema validation
```

### 🧪 **requirements-test.txt** (Testing Dependencies)  
**Purpose**: Dependencies needed for running tests
**Contents**: Testing framework and coverage tools
**Usage**: `pip install -r requirements-test.txt`

```txt
pytest==8.4.2      # Testing framework
pytest-cov==7.0.0  # Coverage reporting
pytest-mock==3.15.1 # Mock utilities
```

### 🔧 **requirements-dev.txt** (Development Dependencies)
**Purpose**: Complete development environment setup
**Contents**: All dependencies for development, testing, and quality tools
**Usage**: `pip install -r requirements-dev.txt` (recommended for developers)

```txt
-r requirements.txt     # Runtime dependencies
-r requirements-test.txt # Testing dependencies
flake8==7.3.0          # Linting
black==25.9.0          # Code formatting
safety==3.2.10        # Security scanning
```

## Pinning Strategy

### ✅ **Exact Version Pinning** 
We use **exact versions** (`==`) rather than ranges (`>=`) for:
- **Security**: Prevent supply chain attacks through dependency confusion
- **Reproducibility**: Identical builds across all environments
- **Stability**: Avoid unexpected changes from automatic updates
- **CI/CD Reliability**: Consistent test environments

### 📅 **Update Policy**
- **Monthly**: Review dependency updates for security patches
- **Quarterly**: Major dependency updates with testing
- **Immediately**: Security vulnerability patches
- **Before Release**: Comprehensive dependency audit

## Security Considerations

### 🛡️ **Vulnerability Monitoring**
```bash
# Check for vulnerabilities
pip install safety
safety check

# Automated in CI/CD
safety check --json --output safety-report.json
```

### 🔒 **License Compliance**
```bash
# Check license compatibility  
pip install pip-licenses
pip-licenses --fail-on GPL --fail-on GPLv2

# Generate compliance report
pip-licenses --format=markdown > license-report.md
```

### 🚫 **Prohibited Dependencies**
- **GPL-licensed packages** (incompatible with MIT license)
- **Packages with known vulnerabilities** (must be updated or replaced)
- **Unmaintained packages** (no updates in 2+ years)
- **Packages with unclear licensing** (must investigate before use)

## Development Workflow

### 🆕 **Adding New Dependencies**

1. **Evaluate necessity**
   ```bash
   # Can this be done with stdlib?
   # Is this the best-maintained option?
   # What's the license?
   ```

2. **Check license compatibility**
   ```bash
   pip show package-name | grep License
   ```

3. **Install and test**
   ```bash
   pip install package-name==specific-version
   python -m pytest  # Ensure tests still pass
   ```

4. **Update requirements**
   ```bash
   # Add exact version to appropriate requirements file
   echo "package-name==1.2.3  # Purpose and justification" >> requirements-dev.txt
   ```

### 🔄 **Updating Dependencies**

1. **Check for updates**
   ```bash
   pip list --outdated
   ```

2. **Research changes**
   - Review changelog for breaking changes
   - Check for security fixes
   - Assess impact on our codebase

3. **Update incrementally**
   ```bash
   # Update one dependency at a time
   pip install package-name==new-version
   python -m pytest  # Verify tests pass
   ```

4. **Update requirements file**
   ```bash
   # Update the pinned version
   sed -i 's/package-name==old-version/package-name==new-version/' requirements-*.txt
   ```

### 🧪 **Testing Dependency Changes**

Always test dependency changes thoroughly:
```bash
# Clean environment test
python -m venv test-env
source test-env/bin/activate  # Windows: test-env\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest
python seeding.py --dry-run
deactivate
```

## CI/CD Integration

### 📋 **Automated Checks**
Our CI/CD pipeline automatically:
- Installs exact pinned versions
- Runs security vulnerability scanning
- Checks license compliance
- Validates dependency integrity

### ⚙️ **GitHub Actions Integration**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements-dev.txt
    
- name: Security scan
  run: |
    safety check --json
    pip-licenses --fail-on GPL
```

## Troubleshooting

### 🔧 **Common Issues**

**Dependency conflicts:**
```bash
# Clear cache and reinstall
pip cache purge
pip install --force-reinstall -r requirements-dev.txt
```

**Version compatibility:**
```bash
# Check dependency tree
pip show package-name
pipdeptree --packages package-name
```

**Security vulnerabilities:**
```bash
# Update affected package
pip install package-name==patched-version
# Or find alternative if no patch available
```

## Business-in-a-Box Alignment

### 🎯 **Professional Standards**
- **Reproducible builds** ensure consistent Business-in-a-Box deployments
- **Security compliance** meets enterprise requirements
- **Legal compliance** enables commercial use without restrictions

### 🔄 **Self-Governing Systems**
- **Automated checking** prevents dependency issues
- **Clear policies** reduce manual oversight needs
- **Professional processes** support enterprise credibility

### 📊 **Target Market Support**
- **Minimal dependencies** reduce complexity for resource-constrained organizations
- **Clear documentation** enables teams to understand and maintain dependencies
- **Automated security** protects users from supply chain attacks

---

**Last Updated**: 2025-09-27  
**Next Review**: 2025-12-27  
**Owner**: Development Team

*This policy ensures Meta-Repo Seed maintains professional standards while enabling reliable Business-in-a-Box infrastructure deployment.*
