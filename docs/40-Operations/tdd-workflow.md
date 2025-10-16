# Test-Driven Development (TDD) Workflow

**Version**: 2.0
**Last Updated**: 2025-10-16
**Purpose**: TDD practices and standards for Meta-Repo-Seed platform

---

## 🎯 Overview

This guide establishes our Test-Driven Development practices for the Meta-Repo-Seed commercial SaaS platform. We follow the **Red-Green-Refactor** cycle with strict quality gates and comprehensive coverage requirements.

---

## 🔄 TDD Cycle

### 1. 🔴 Red Phase: Write Failing Test
- Write a test that describes the desired behavior
- Ensure the test fails for the right reason
- Commit the failing test

### 2. 🟢 Green Phase: Make Test Pass
- Write minimal code to make the test pass
- Don't worry about code quality yet
- Commit the passing test

### 3. 🔄 Refactor Phase: Improve Code
- Improve code quality while keeping tests green
- Refactor for readability, performance, and maintainability
- Commit the refactored code

---

## 📊 Coverage Standards

### Minimum Requirements
- **Unit Tests**: 95% code coverage
- **Integration Tests**: All critical workflows covered
- **API Tests**: All endpoints tested
- **Security Tests**: All security features tested
- **Overall**: 90% total coverage

### Current Status
```bash
# Check current coverage
python -m pytest --cov=src/commercial --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov-report=html:htmlcov
# Open htmlcov/index.html in browser
```

---

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions/methods in isolation
**Scope**: Single function, class, or module
**Dependencies**: Mocked external dependencies
**Speed**: Fast execution (< 1 second per test)

```python
# Example unit test
def test_customer_creation():
    """Test customer creation with valid data."""
    # Arrange
    customer_manager = CustomerManager()

    # Act
    customer = customer_manager.create_customer(
        email="test@example.com",
        company_name="Test Company"
    )

    # Assert
    assert customer.email == "test@example.com"
    assert customer.company_name == "Test Company"
    assert customer.status == CustomerStatus.ACTIVE
```

### Integration Tests (`tests/integration/`)
**Purpose**: Test component interactions
**Scope**: Multiple components working together
**Dependencies**: Real database, file system
**Speed**: Medium execution (1-10 seconds per test)

```python
# Example integration test
def test_organization_deployment():
    """Test complete organization deployment workflow."""
    # Arrange
    customer = create_test_customer()
    seeder = OrganizationSeeder.create_for_customer(
        customer.customer_id,
        "Test Organization"
    )

    # Act
    result = seeder.deploy_organization()

    # Assert
    assert result.success is True
    assert result.organization.status == OrganizationStatus.ACTIVE
```

### End-to-End Tests (`tests/e2e/`)
**Purpose**: Test complete user workflows
**Scope**: Full system from user input to final output
**Dependencies**: Complete system, external services
**Speed**: Slow execution (10+ seconds per test)

```python
# Example E2E test
def test_customer_onboarding_workflow():
    """Test complete customer onboarding from signup to deployment."""
    # Arrange
    test_data = {
        "email": "newcustomer@example.com",
        "company_name": "New Company",
        "plan": "startup"
    }

    # Act
    response = client.post("/api/customers", json=test_data)
    customer_id = response.json()["customer_id"]

    # Deploy organization
    deploy_response = client.post(f"/api/organizations/{customer_id}/deploy")

    # Assert
    assert response.status_code == 201
    assert deploy_response.status_code == 200
    assert deploy_response.json()["status"] == "deployed"
```

---

## 🔧 Test Infrastructure

### Test Database
```python
# conftest.py
@pytest.fixture
def test_db():
    """Create test database for integration tests."""
    db_url = "postgresql://test:test@localhost/test_db"
    db_manager = DatabaseManager(db_url)
    db_manager.create_tables()
    yield db_manager
    db_manager.cleanup()
```

### Test Data Factories
```python
# test_factories.py
def create_test_customer(**kwargs):
    """Create test customer with default values."""
    defaults = {
        "email": "test@example.com",
        "company_name": "Test Company",
        "plan": SubscriptionPlan.STARTUP
    }
    defaults.update(kwargs)
    return Customer(**defaults)
```

### Mock External Services
```python
# test_mocks.py
@pytest.fixture
def mock_github_api():
    """Mock GitHub API for testing."""
    with patch('src.integrations.github.GitHubAPI') as mock:
        mock.return_value.create_repository.return_value = {
            "id": "test-repo-id",
            "name": "test-repo",
            "url": "https://github.com/test/test-repo"
        }
        yield mock
```

---

## 📋 TDD Checklist

### Before Writing Code
- [ ] **Understand requirements** - What should this code do?
- [ ] **Write failing test** - Test the desired behavior
- [ ] **Run test** - Confirm it fails for the right reason
- [ ] **Commit failing test** - Document the requirement

### During Implementation
- [ ] **Write minimal code** - Just enough to make test pass
- [ ] **Run test** - Confirm it now passes
- [ ] **Commit passing test** - Document the implementation
- [ ] **Refactor** - Improve code quality while keeping tests green
- [ ] **Run all tests** - Ensure no regressions

### After Implementation
- [ ] **Check coverage** - Ensure adequate test coverage
- [ ] **Review tests** - Are they clear and maintainable?
- [ ] **Update documentation** - Reflect any changes in behavior
- [ ] **Clean up** - Remove any temporary test data

---

## 🚨 Common TDD Anti-Patterns

### ❌ **Don't Do This**
- **Write tests after code** - Defeats the purpose of TDD
- **Skip the red phase** - Tests should fail first
- **Write overly complex tests** - Keep tests simple and focused
- **Ignore failing tests** - Fix or remove, never ignore
- **Test implementation details** - Test behavior, not implementation

### ✅ **Do This Instead**
- **Write tests first** - Before any implementation
- **Make tests fail first** - Red phase is crucial
- **Keep tests simple** - One assertion per test when possible
- **Fix failing tests immediately** - Don't let them accumulate
- **Test public interfaces** - Focus on behavior, not internals

---

## 🔍 Test Quality Guidelines

### Test Naming
```python
# Good: Descriptive test names
def test_customer_creation_with_valid_email():
def test_organization_deployment_fails_with_invalid_config():
def test_subscription_upgrade_changes_plan():

# Bad: Vague test names
def test_customer():
def test_deployment():
def test_upgrade():
```

### Test Structure
```python
def test_feature_behavior():
    """Test description explaining what this tests."""
    # Arrange - Set up test data and conditions
    customer = create_test_customer(email="test@example.com")

    # Act - Execute the code being tested
    result = customer_manager.validate_customer(customer)

    # Assert - Verify the expected outcome
    assert result.is_valid is True
    assert result.errors == []
```

### Test Data Management
```python
# Good: Use factories for test data
def test_customer_validation():
    customer = CustomerFactory.create(email="test@example.com")
    # ... test logic

# Bad: Hardcode test data everywhere
def test_customer_validation():
    customer = Customer(
        customer_id="cust_123",
        email="test@example.com",
        company_name="Test Company",
        # ... many more fields
    )
```

---

## 📊 Coverage Monitoring

### Coverage Reports
```bash
# Generate coverage report
python -m pytest --cov=src --cov-report=html --cov-report=term

# Check specific modules
python -m pytest --cov=src/commercial --cov-report=term-missing

# Coverage threshold enforcement
python -m pytest --cov=src --cov-fail-under=90
```

### Coverage Goals
- **New Code**: 100% coverage required
- **Modified Code**: 95% coverage required
- **Legacy Code**: 80% coverage minimum
- **Critical Paths**: 100% coverage required

---

## 🔄 Continuous Integration

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: python -m pytest tests/unit/
        language: system
        pass_filenames: false
        always_run: true
```

### CI Pipeline
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: python -m pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 🆘 Troubleshooting

### Common Issues

#### Tests Fail Intermittently
- **Cause**: Race conditions, shared state
- **Solution**: Use proper test isolation, mock external dependencies

#### Slow Test Execution
- **Cause**: Real database, file I/O, network calls
- **Solution**: Use mocks, test database, in-memory storage

#### High Test Maintenance
- **Cause**: Tests coupled to implementation details
- **Solution**: Test behavior, not implementation

#### Coverage Gaps
- **Cause**: Missing test cases, untested error paths
- **Solution**: Add edge case tests, error condition tests

---

## 📚 Related Documents

- [Development Workflow](development-workflow.md) - Overall development process
- [Code Quality Standards](code-quality-standards.md) - Code style and standards
- [Testing Strategy](testing-strategy.md) - Testing approach and tools
- [CI/CD Pipeline](ci-cd-pipeline.md) - Continuous integration setup

---

**This TDD workflow ensures high-quality, reliable code through comprehensive testing practices.**
