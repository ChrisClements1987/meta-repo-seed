module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Custom scopes for Business-in-a-Box project
    'scope-enum': [2, 'always', [
      // Business-in-a-Box specific scopes
      'business',     // Business profile and deployment functionality  
      'cli',          // Command-line interface
      'templates',    // Template generation and processing
      'auth',         // Authentication and authorization
      'deploy',       // Deployment and infrastructure
      'api',          // API endpoints and interfaces
      'config',       // Configuration management
      
      // Technical scopes
      'ci',           // Continuous integration
      'deps',         // Dependencies
      'security',     // Security-related changes
      'performance',  // Performance optimizations
      'docs',         // Documentation (when used as scope)
      'test',         // Testing (when used as scope)
      'build',        // Build system
      
      // Infrastructure scopes
      'docker',       // Docker and containerization
      'k8s',          // Kubernetes configurations
      'terraform',    // Infrastructure as Code
      'monitoring',   // Monitoring and observability
      
      // Process scopes
      'audit',        // Audit and compliance
      'analysis',     // Analysis and research
      'workflow',     // Development workflow changes
    ]],
    
    // Subject line length (GitHub shows ~50 chars in summaries)
    'subject-max-length': [2, 'always', 50],
    
    // Body line length for readability
    'body-max-line-length': [2, 'always', 72],
    
    // Required types for our workflow
    'type-enum': [2, 'always', [
      // Primary types
      'feat',      // New feature
      'fix',       // Bug fix
      'docs',      // Documentation changes
      'style',     // Code formatting (no logic change)
      'refactor',  // Code refactoring
      'test',      // Test changes
      'chore',     // Build/tooling changes
      
      // Extended types
      'perf',      // Performance improvements
      'build',     // Build system changes
      'ci',        // CI/CD changes
      'revert',    // Revert previous commit
      
      // Business-in-a-Box specific types
      'hotfix',    // Emergency production fixes
      'analysis',  // Analysis and research work
      'audit',     // Audit documentation
    ]],
    
    // Subject must be lowercase (conventional)
    'subject-case': [2, 'always', 'lower-case'],
    
    // No period at end of subject
    'subject-full-stop': [2, 'never', '.'],
    
    // Empty line between subject and body
    'body-leading-blank': [2, 'always'],
    
    // Empty line between body and footer
    'footer-leading-blank': [2, 'always'],
    
    // Type must be lowercase
    'type-case': [2, 'always', 'lower-case'],
    
    // Scope must be lowercase
    'scope-case': [2, 'always', 'lower-case'],
    
    // No empty scope (either have scope or don't)
    'scope-empty': [0], // Allow both scoped and unscoped commits
  },
  
  // Custom prompt configuration for interactive commits
  prompt: {
    questions: {
      type: {
        description: 'Select the type of change that you\'re committing',
        enum: {
          feat: {
            description: 'A new feature for users',
            title: 'Features',
            emoji: '✨',
          },
          fix: {
            description: 'A bug fix that affects users',
            title: 'Bug Fixes',
            emoji: '🐛',
          },
          docs: {
            description: 'Documentation changes only',
            title: 'Documentation',
            emoji: '📚',
          },
          style: {
            description: 'Changes that do not affect the meaning of the code (formatting, etc)',
            title: 'Styles',
            emoji: '💎',
          },
          refactor: {
            description: 'A code change that neither fixes a bug nor adds a feature',
            title: 'Code Refactoring',
            emoji: '📦',
          },
          perf: {
            description: 'A code change that improves performance',
            title: 'Performance Improvements',
            emoji: '🚀',
          },
          test: {
            description: 'Adding missing tests or correcting existing tests',
            title: 'Tests',
            emoji: '🚨',
          },
          build: {
            description: 'Changes that affect the build system or external dependencies',
            title: 'Builds',
            emoji: '🛠',
          },
          ci: {
            description: 'Changes to our CI configuration files and scripts',
            title: 'Continuous Integrations',
            emoji: '⚙️',
          },
          chore: {
            description: 'Other changes that don\'t modify src or test files',
            title: 'Chores',
            emoji: '♻️',
          },
          revert: {
            description: 'Reverts a previous commit',
            title: 'Reverts',
            emoji: '🗑',
          },
          hotfix: {
            description: 'Emergency fix for production issues',
            title: 'Hotfixes',
            emoji: '🚨',
          },
          analysis: {
            description: 'Analysis and research work',
            title: 'Analysis',
            emoji: '📊',
          },
          audit: {
            description: 'Audit documentation and compliance',
            title: 'Audits',
            emoji: '🔍',
          },
        },
      },
      scope: {
        description: 'What is the scope of this change (e.g. business, cli, templates)',
      },
      subject: {
        description: 'Write a short, imperative tense description of the change (max 50 chars)',
      },
      body: {
        description: 'Provide a longer description of the change (optional). Use "|" for line breaks',
      },
      isBreaking: {
        description: 'Are there any breaking changes?',
        default: false,
      },
      breakingBody: {
        description: 'A BREAKING CHANGE commit requires a body. Please enter a longer description of the commit itself',
      },
      breaking: {
        description: 'Describe the breaking changes',
      },
      isIssueAffected: {
        description: 'Does this change affect any open issues?',
        default: false,
      },
      issuesBody: {
        description: 'If issues are closed, the commit requires a body. Please enter a longer description of the commit itself',
      },
      issues: {
        description: 'Add issue references (e.g. "fix #123", "re #123")',
      },
    },
  },
};
