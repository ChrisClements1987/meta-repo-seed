# Test-Driven Development Guide

This guide establishes test-first development practices for the Meta-Repo Seeding System.

## 🎯 TDD Philosophy

We follow the **Red-Green-Refactor** cycle:
1. **🔴 Red**: Write a failing test first
2. **🟢 Green**: Write minimal code to make it pass  
3. **🔄 Refactor**: Improve code while keeping tests green

## 📊 Coverage Standards

### Minimum Requirements
- **Unit Tests**: 95% code coverage
- **Integration Tests**: All critical workflows covered
- **Security Tests**: All security features tested
- **Overall**: 90% total coverage (current: 54%)

### Current Status
```bash
# Check current coverage
pytest tests/unit/ --cov=seeding --cov=src --cov-report=term-missing

# Generate HTML coverage report
pytest --cov-report=html:htmlcov
# Open htmlcov/index.html in browser
```

## 🧪 Testing Strategy

### Test Types

#### 1. Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions in isolation
**Coverage**: 95%+ required
**Location**: `tests/unit/test_*.py`

```python
def test_sanitize_project_name_valid_input():
    """Test that valid project names pass validation."""
    result = sanitize_project_name("valid-project-123")
    assert result == "valid-project-123"

def test_sanitize_project_name_blocks_traversal():
    """Test that path traversal attempts are blocked."""
    with pytest.raises(ValueError, match="path separators"):
        sanitize_project_name("../malicious-path")
```

#### 2. Integration Tests (`tests/integration/`)
**Purpose**: Test component interactions
**Coverage**: All major workflows
**Location**: `tests/integration/test_*.py`

#### 3. Security Tests (`tests/security/`)
**Purpose**: Test security protections
**Coverage**: All security features
**Location**: `tests/security/test_*.py` (TO BE CREATED)

## 🔄 TDD Workflow

### For New Features
1. **Write Test First**
   ```bash
   # Create test file
   touch tests/unit/test_new_feature.py
   
   # Write failing test
   def test_new_feature_behavior():
       # Test the expected behavior
       assert new_feature() == expected_result
   ```

2. **Run Tests (Should Fail)**
   ```bash
   pytest tests/unit/test_new_feature.py -v
   # Should show RED - test fails because function doesn't exist
   ```

3. **Implement Minimal Code**
   ```python
   def new_feature():
       return expected_result  # Minimal implementation
   ```

4. **Run Tests (Should Pass)**
   ```bash
   pytest tests/unit/test_new_feature.py -v
   # Should show GREEN - test passes
   ```

5. **Refactor and Improve**
   - Improve implementation while keeping tests green
   - Add edge case tests
   - Ensure coverage requirements met

### For Bug Fixes
1. **Write Reproducing Test**
   ```python
   def test_bug_reproduction():
       """Test that reproduces the reported bug."""
       # This test should fail initially
       assert buggy_function() == correct_behavior
   ```

2. **Fix the Bug**
   - Modify code to make test pass
   - Ensure no existing tests break

3. **Add Regression Tests**
   - Test edge cases around the bug
   - Prevent future regressions

## 🛠️ Testing Infrastructure

### Required Dependencies
```bash
pip install pytest pytest-cov pytest-mock
```

### Test Configuration (`pytest.ini`)
```ini
[tool:pytest]
addopts = 
    -v
    --tb=short
    --cov=seeding
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=90
```

### Pre-Commit Hooks (`.pre-commit-config.yaml`)
```yaml
repos:
- repo: local
  hooks:
  - id: pytest
    name: pytest
    entry: pytest
    language: python
    pass_filenames: false
    always_run: true
```

## 📁 Test Organization

```
tests/
├── unit/                    # Individual function tests
│   ├── test_seeding.py     # Core seeding functions
│   ├── test_configuration.py # Configuration management
│   ├── test_templates.py   # Template processing
│   └── test_security.py    # Security function tests (NEW)
├── integration/             # Component interaction tests
│   ├── test_full_workflow.py
│   └── test_github_integration.py
├── security/               # Security-focused tests (NEW)
│   ├── test_path_traversal.py
│   ├── test_symlink_protection.py
│   └── test_input_validation.py
├── fixtures/               # Test data and templates
│   ├── templates/
│   └── structures/
└── conftest.py             # Shared test configuration
```

## 🚀 Quick Start TDD Example

### Scenario: Adding a new feature
```python
# 1. Write test first (RED)
def test_validate_github_username():
    \"\"\"Test GitHub username validation.\"\"\"
    # Should accept valid usernames
    assert validate_github_username("valid-user-123") == True
    
    # Should reject invalid characters
    with pytest.raises(ValueError):
        validate_github_username("invalid user!")

# 2. Run test (should fail)
pytest tests/unit/test_validation.py::test_validate_github_username -v

# 3. Implement function (GREEN)
def validate_github_username(username: str) -> bool:
    import re
    if not re.match(r"^[a-zA-Z0-9-]+$", username):
        raise ValueError("Invalid GitHub username")
    return True

# 4. Run test (should pass)
pytest tests/unit/test_validation.py::test_validate_github_username -v

# 5. Refactor and add edge cases
def test_validate_github_username_edge_cases():
    # Test various edge cases...
```

## 📋 Current Action Items

### Immediate (This Sprint)
- [ ] Fix Configuration class interface (#49)
- [ ] Update function behavior tests  
- [ ] Enable coverage reporting
- [ ] Achieve 75% coverage baseline

### Short-term (Next Sprint)
- [ ] Create security test suite
- [ ] Implement TDD workflow standards
- [ ] Add pre-commit test hooks
- [ ] Reach 85% coverage

### Medium-term (Month)
- [ ] 90%+ coverage target
- [ ] Comprehensive integration tests
- [ ] Performance test suite
- [ ] TDD training documentation

## 🎓 TDD Best Practices

1. **Write Tests First** - Always start with failing tests
2. **Small Steps** - Write minimal code to pass each test
3. **Refactor Fearlessly** - Tests provide safety net
4. **Test Edge Cases** - Include error conditions and boundaries
5. **Maintain Fast Tests** - Unit tests should run in seconds
6. **Isolate Dependencies** - Use mocks for external systems
7. **Descriptive Names** - Test names should explain behavior clearly

*Ready to transform development practices with test-first approach!* 🚀
