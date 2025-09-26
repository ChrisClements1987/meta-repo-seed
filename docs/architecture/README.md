# Architecture Documentation

This directory contains architectural documentation for the Meta-Repo Seeding System.

## 📁 Structure

- **`adr/`** - Architecture Decision Records (ADRs)
- **`cli.md`** - Command Line Interface contract and specifications
- **`system-overview.md`** - High-level system architecture
- **`security.md`** - Security architecture and considerations

## 🏗️ Architecture Overview

The Meta-Repo Seeding System follows a modular architecture designed for:

- **Idempotent Operations** - Safe to run multiple times
- **Cross-Platform Support** - Windows, macOS, Linux compatibility
- **Template-Driven Generation** - Flexible content generation
- **Security-First Design** - Path traversal protection and input sanitization

## 🔄 Architecture Decision Records (ADRs)

ADRs document significant architectural decisions made during development:

- [ADR-001: Template System Architecture](adr/001-template-system.md) (planned)
- [ADR-002: Security Model](adr/002-security-model.md) (planned)
- [ADR-003: CLI Design](adr/003-cli-design.md) (planned)

## 📊 Key Design Principles

1. **Business-in-a-Box Focus** - Every component serves the 10-minute deployment goal
2. **Professional Standards** - Enterprise-grade quality in all outputs
3. **Self-Governing Systems** - Automated compliance and quality enforcement
4. **Incremental Adoption** - Support legacy systems while encouraging modern practices
5. **AI-Assisted Development** - Clear patterns for AI understanding and assistance

## 🔗 Related Documentation

- [CLI Reference](../reference/cli.md)
- [API Reference](../reference/api.md)
- [Development Workflow](../development/workflow-standards.md)
- [Contributing Guide](../development/contributing.md)
