# CLI Contract and Specifications

This document defines the command-line interface contract for the Meta-Repo Seeding System.

## 🎯 CLI Philosophy

The CLI follows these principles:
- **Consistent naming** - Predictable flag names and conventions
- **Backward compatibility** - Changes maintain compatibility or provide deprecation path
- **Clear defaults** - Sensible defaults for common use cases
- **Composable** - Flags work together logically

## 🚀 Main Command: seeding.py

### Synopsis
```bash
python seeding.py [OPTIONS]
```

### Options

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--project` | | string | auto-detect | Project name for template replacement |
| `--username` | | string | from git/env | GitHub username for template replacement |
| `--dry-run` | | boolean | false | Preview changes without making them |
| `--verbose` | `-v` | boolean | false | Enable detailed logging |
| `--config` | | path | none | Load configuration from file |
| `--save-config` | | path | none | Save current settings to configuration file |
| `--list-configs` | | boolean | false | List available configuration files |
| `--template-path` | | path | auto-detect | Path to templates directory |
| `--help` | `-h` | boolean | false | Show help message |

### Examples

```bash
# Basic usage
python seeding.py

# Preview mode
python seeding.py --dry-run --verbose

# Custom parameters
python seeding.py --project myproject --username myuser

# Configuration file usage
python seeding.py --config my-project.yaml
python seeding.py --save-config team-config.yaml --project shared-project

# List configurations
python seeding.py --list-configs
```

## 🔧 Environment Variables

| Variable | Description | Usage |
|----------|-------------|-------|
| `GITHUB_USERNAME` | GitHub username for authentication | CI/CD pipelines, non-interactive environments |

## 🔄 Backward Compatibility

### Current Stable Interface (v1.0.0)
- All current flags are stable and will be maintained
- New flags will be additive only
- Deprecation warnings will be provided before removing any flags

### Deprecation Policy
1. **Warning Phase** - 2 minor releases with deprecation warnings
2. **Documentation Phase** - Update docs to show new preferred usage
3. **Removal Phase** - Remove in next major version

## 🧪 Testing Requirements

All CLI changes must include:
- [ ] Unit tests for argument parsing
- [ ] Integration tests for flag combinations
- [ ] Help text verification
- [ ] Error handling tests

### Test Examples

```python
def test_cli_basic_args():
    """Test basic argument parsing."""
    args = parse_arguments(['--project', 'test', '--dry-run'])
    assert args.project == 'test'
    assert args.dry_run is True

def test_cli_config_override():
    """Test config file with CLI overrides."""
    # Test implementation
```

## 📝 Adding New Options

When adding new CLI options:

1. **Design Phase**
   - Follow naming conventions (kebab-case for multi-word flags)
   - Consider flag grouping and logical relationships
   - Plan default values and environment variable support

2. **Implementation Phase**
   - Update argparse configuration
   - Add validation and error handling
   - Update help text and documentation

3. **Testing Phase**
   - Add unit tests for new options
   - Test interaction with existing options
   - Verify help text and error messages

4. **Documentation Phase**
   - Update this CLI contract document
   - Update README and user guides
   - Add examples of new option usage

## 🚨 Breaking Changes

Breaking changes require:
- Major version bump
- Migration guide in CHANGELOG
- Deprecation period for removed features
- Clear communication in release notes

## 🔍 Validation Rules

CLI validation enforces:
- **Project names**: Letters, numbers, hyphens, underscores, periods only
- **Paths**: No parent directory traversal (`../`)
- **Configuration**: Valid YAML/JSON format
- **Combinations**: Mutually exclusive options handled gracefully

## 🎨 Output Formatting

CLI output follows these standards:
- **Progress indicators** for long operations
- **Colored output** where supported (with --no-color option)
- **Machine-readable** formats available (JSON, YAML)
- **Consistent** error message formatting

## 📊 Exit Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 0 | Success | Operation completed successfully |
| 1 | General error | Configuration issues, file not found |
| 2 | CLI usage error | Invalid arguments or options |
| 3 | Template error | Template processing failed |
| 4 | Permission error | Insufficient permissions |

## 🔗 Related Documentation

- [Configuration Guide](../guides/configuration.md)
- [Template System](../guides/templates.md)
- [API Reference](../reference/api.md)
- [Troubleshooting](../guides/troubleshooting.md)
