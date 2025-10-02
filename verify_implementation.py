#!/usr/bin/env python3
"""
Verify the business operations automation implementation.
"""

import sys
import asyncio
import tempfile
from pathlib import Path

# Add the module to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "automation"))

def test_imports():
    """Test that all imports work correctly."""
    print("Testing imports...")
    
    try:
        from business_operations import (
            BusinessOperationsManager,
            BusinessOperationsConfig,
            BusinessProfile,
            AutomationLevel,
            deploy_business_operations_automation
        )
        print("SUCCESS: All imports successful")
        return True
    except Exception as e:
        print(f"ERROR: Import failed - {e}")
        return False

def test_configuration():
    """Test configuration creation."""
    print("Testing configuration...")
    
    try:
        from business_operations import BusinessOperationsConfig, BusinessProfile, AutomationLevel
        
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.STARTUP_BASIC,
            automation_level=AutomationLevel.STANDARD
        )
        
        assert config.business_profile == BusinessProfile.STARTUP_BASIC
        assert config.automation_level == AutomationLevel.STANDARD
        assert config.self_healing_enabled == True
        
        print("SUCCESS: Configuration test passed")
        return True
    except Exception as e:
        print(f"ERROR: Configuration test failed - {e}")
        return False

async def test_deployment():
    """Test automation deployment."""
    print("Testing deployment...")
    
    try:
        from business_operations import deploy_business_operations_automation
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = await deploy_business_operations_automation(
                target_dir=Path(temp_dir),
                org_name="test-org",
                repo_name="test-repo",
                business_profile="startup-basic",
                automation_level="standard",
                dry_run=True
            )
            
            assert 'overall_success' in result
            assert 'business_profile' in result
            assert result['business_profile'] == 'startup-basic'
            
            print("SUCCESS: Deployment test passed")
            print(f"  - Success: {result['overall_success']}")
            print(f"  - Components: {len(result.get('components_deployed', {}))}")
            return True
            
    except Exception as e:
        print(f"ERROR: Deployment test failed - {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all verification tests."""
    print("Business Operations Automation - Implementation Verification")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports()),
        ("Configuration Test", test_configuration()),
        ("Deployment Test", test_deployment())
    ]
    
    results = []
    for test_name, test_result in tests:
        print(f"\n{test_name}:")
        if asyncio.iscoroutine(test_result):
            result = await test_result
        else:
            result = test_result
        results.append(result)
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print("=" * 60)
    
    for i, (test_name, _) in enumerate(tests):
        status = "PASS" if results[i] else "FAIL"
        print(f"{status}: {test_name}")
    
    passed = sum(results)
    total = len(results)
    print(f"\nResult: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\nSUCCESS: Business Operations Automation implementation is working!")
        return 0
    else:
        print("\nERROR: Some tests failed.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
