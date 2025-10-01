#!/usr/bin/env python3
"""
Simple verification script for Issue #97: Infrastructure as Code Templates
"""

import tempfile
import shutil
import logging
from pathlib import Path
from seeding import RepoSeeder

# Set up logging to avoid issues
logging.basicConfig(level=logging.INFO)

def verify_infrastructure():
    """Verify infrastructure templates are working."""
    
    print("Verifying Infrastructure as Code Templates Implementation (Issue #97)")
    print("=" * 80)
    
    # Test configuration
    test_dir = Path(tempfile.mkdtemp())
    seeder = RepoSeeder(
        project_name="test-verification",
        github_username="test-user",
        dry_run=False
    )
    seeder.base_path = test_dir
    seeder.project_root = seeder.base_path / "test-verification"
    seeder.meta_repo_path = seeder.project_root / 'meta-repo'
    
    try:
        # Run infrastructure template creation
        print("Creating infrastructure templates...")
        seeder.create_infrastructure_templates()
        
        # Verify core components
        infrastructure_path = seeder.meta_repo_path / 'infrastructure'
        
        checks = []
        
        # Check directories exist
        dirs = ['terraform', 'kubernetes', 'docker', 'environments', 'monitoring', 'scripts', 'business-profiles']
        for d in dirs:
            checks.append((f"{d} directory", (infrastructure_path / d).exists()))
        
        # Check key files exist
        files = [
            'terraform/main.tf',
            'kubernetes/deployment.yaml', 
            'docker/Dockerfile.template',
            'monitoring/prometheus.yml',
            'scripts/deploy-infrastructure.sh',
            'business-profiles/startup-basic-infrastructure.yml'
        ]
        for f in files:
            checks.append((f"File {f}", (infrastructure_path / f).exists()))
        
        # Print results
        all_passed = True
        for check_name, passed in checks:
            status = "[OK]" if passed else "[FAIL]"
            print(f"    {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n[SUCCESS] All infrastructure components verified!")
            print("Issue #97 implementation is complete and working.")
            return True
        else:
            print("\n[FAIL] Some components missing.")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False
        
    finally:
        if test_dir.exists():
            shutil.rmtree(test_dir)

if __name__ == "__main__":
    success = verify_infrastructure()
    exit(0 if success else 1)
