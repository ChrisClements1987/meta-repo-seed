#!/usr/bin/env python3
"""Environment Validation Script - Prevents drift across workspaces"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    version_file = Path(".python-version")
    if not version_file.exists():
        print("[FAIL] Missing .python-version file")
        return False
    
    required = version_file.read_text().strip()
    current = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    if current != required:
        print(f"[FAIL] Python mismatch: {current} != {required}")
        return False
    
    print(f"[PASS] Python version: {current}")
    return True


def check_dependencies():
    try:
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True, check=True)
        installed = {line.split("==")[0] for line in result.stdout.split("\n") if "==" in line}
        
        critical = ["pytest", "pytest-cov", "pytest-mock", "pytest-asyncio"]
        missing = [dep for dep in critical if dep not in installed]
        
        if missing:
            print(f"[FAIL] Missing: {', '.join(missing)}")
            return False
        
        print("[PASS] All critical dependencies installed")
        return True
    except:
        print("[FAIL] Could not check dependencies")
        return False


def main():
    print("Validating development environment...\n")
    
    checks = [check_python_version, check_dependencies]
    results = [check() for check in checks]
    
    print()
    if all(results):
        print("[SUCCESS] Environment validated")
        return 0
    else:
        print("[FAILED] Environment validation failed")
        print("Run: pip install -r requirements-test.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
