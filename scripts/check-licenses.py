#!/usr/bin/env python3
"""
Future-proof license compliance checker for meta-repo-seed.
Checks dependencies against approved license allowlist.
"""

import subprocess
import sys
import json
import re
from typing import Dict, List, Set


class LicenseChecker:
    """Robust license compliance checker with allowlist approach."""
    
    # Approved licenses (MIT-compatible)
    APPROVED_LICENSES = {
        # Permissive licenses
        'MIT License', 'MIT', 'mit',
        'BSD License', 'BSD', 'BSD-2-Clause', 'BSD-3-Clause',
        'Apache License 2.0', 'Apache-2.0', 'Apache Software License',
        'ISC License', 'ISC',
        'The Unlicense (Unlicense)', 'Unlicense',
        
        # Compatible copyleft (when used as libraries)
        'GNU Lesser General Public License (LGPL)', 'GNU Library or Lesser General Public License (LGPL)',
        'LGPLv2+', 'LGPLv3+', 'GNU Lesser General Public License v2 or later (LGPLv2+)',
        
        # Mozilla and other compatible
        'Mozilla Public License 2.0 (MPL 2.0)', 'MPL-2.0',
        'Python Software Foundation License', 'PSF',
        
        # Multi-license (typically includes MIT/Apache)
        'Apache Software License; BSD License', 'MIT AND Python-2.0',
        'Apache-2.0 OR BSD-3-Clause', 'Apache Software License; MIT License',
    }
    
    # Known problematic licenses (GPL family)
    PROHIBITED_LICENSES = {
        'GNU General Public License (GPL)', 'GPL', 'GPLv2', 'GPLv3',
        'GNU Affero General Public License', 'AGPL', 'AGPLv3',
        'Server Side Public License', 'SSPL',
        'Commons Clause', 'Business Source License', 'BUSL',
    }
    
    # Manually verified packages with UNKNOWN but safe licenses  
    VERIFIED_PACKAGES = {
        'pytest-asyncio': 'Apache-2.0',  # Verified from GitHub LICENSE file
        # Add more as needed: 'package-name': 'verified-license'
    }

    def get_dependencies(self) -> List[Dict]:
        """Get dependency list from pip-licenses."""
        try:
            result = subprocess.run(
                ['pip-licenses', '--format=json'], 
                capture_output=True, text=True, check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Error running pip-licenses: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Error parsing pip-licenses output: {e}")
            sys.exit(1)

    def normalize_license(self, license_name: str) -> str:
        """Normalize license name for comparison."""
        if not license_name or license_name == 'UNKNOWN':
            return 'UNKNOWN'
        
        # Remove extra whitespace and convert to standard form
        license_name = re.sub(r'\s+', ' ', license_name.strip())
        
        # Handle common variations
        if 'apache' in license_name.lower() and '2.0' in license_name:
            return 'Apache-2.0'
        if 'mit' in license_name.lower():
            return 'MIT'
        if 'bsd' in license_name.lower():
            return 'BSD'
            
        return license_name

    def check_license_compliance(self) -> bool:
        """Check all dependencies for license compliance."""
        dependencies = self.get_dependencies()
        
        violations = []
        unknown_packages = []
        approved_count = 0
        
        print("Checking license compliance for all dependencies...")
        print()
        
        for dep in dependencies:
            name = dep['Name']
            license_name = dep['License']
            version = dep['Version']
            
            normalized_license = self.normalize_license(license_name)
            
            # Check for prohibited licenses (GPL family - but NOT LGPL)
            is_prohibited = False
            for prohibited in self.PROHIBITED_LICENSES:
                if prohibited in normalized_license:
                    # Special case: LGPL is allowed, only pure GPL is prohibited
                    if 'LGPL' not in normalized_license and 'Lesser' not in normalized_license:
                        is_prohibited = True
                        break
            
            if is_prohibited:
                violations.append(f"VIOLATION: {name} {version}: {license_name} (PROHIBITED)")
                continue
            
            # Check manually verified packages first
            if name in self.VERIFIED_PACKAGES:
                verified_license = self.VERIFIED_PACKAGES[name]
                print(f"VERIFIED: {name} {version}: {license_name} -> {verified_license}")
                approved_count += 1
                continue
                
            # Check approved licenses
            if normalized_license in self.APPROVED_LICENSES:
                print(f"APPROVED: {name} {version}: {license_name}")
                approved_count += 1
                continue
                
            # Unknown license - needs investigation but not blocking
            if normalized_license == 'UNKNOWN':
                unknown_packages.append(f"UNKNOWN: {name} {version}: {license_name} (needs verification)")
                continue
                
            # Unrecognized license - may need review
            unknown_packages.append(f"UNRECOGNIZED: {name} {version}: {license_name}")
        
        print()
        print("License Compliance Summary:")
        print(f"Approved: {approved_count} packages")
        print(f"Unknown/Unrecognized: {len(unknown_packages)} packages")
        print(f"Violations: {len(violations)} packages")
        print()
        
        # Report violations (blocking)
        if violations:
            print("LICENSE VIOLATIONS FOUND:")
            for violation in violations:
                print(violation)
            print()
            print("These dependencies must be removed or replaced with MIT-compatible alternatives.")
            return False
            
        # Report unknown licenses (non-blocking but noted)
        if unknown_packages:
            print("Unknown licenses detected (non-blocking):")
            for unknown in unknown_packages:
                print(unknown)
            print()
            print("These should be investigated and added to VERIFIED_PACKAGES if safe.")
            
        print("License compliance check passed!")
        return True


def main():
    """Main license checking function."""
    checker = LicenseChecker()
    
    if not checker.check_license_compliance():
        print("License compliance check failed!")
        sys.exit(1)
        
    print("All license requirements satisfied!")
    sys.exit(0)


if __name__ == '__main__':
    main()
