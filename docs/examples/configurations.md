# Configuration Examples

This document provides practical examples of configuration files for different project types and use cases.

## 🌐 Web Application Projects

### React TypeScript Application

```yaml
# configs/react-typescript-app.yml
project:
  name: "react-typescript-starter"
  description: "Modern React application with TypeScript"
  type: "web-application"
  framework: "react-typescript"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["react", "typescript", "web-app", "frontend"]
  
  repository:
    has_issues: true
    has_projects: true
    has_wiki: false
    
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "React TypeScript Application"
  TECH_STACK: "React, TypeScript, Vite, Tailwind CSS"
  NODE_VERSION: "18"
  DEPLOYMENT_TARGET: "Vercel"
  
options:
  verbose: true
  backup_existing: true
```

### Next.js Full-Stack Application

```yaml
# configs/nextjs-fullstack.yml
project:
  name: "nextjs-fullstack-app"
  description: "Full-stack Next.js application with API routes"
  type: "fullstack-web-application"
  framework: "nextjs"

github:
  enabled: true
  create_repo: true
  private: true
  branch_protection: true
  
  branch_protection:
    required_reviews: 1
    dismiss_stale_reviews: true
    required_status_checks:
      - "ci/build"
      - "ci/test"
      - "vercel"
    
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Full-Stack Web Application"
  TECH_STACK: "Next.js, TypeScript, Prisma, PostgreSQL"
  NODE_VERSION: "18"
  DEPLOYMENT_TARGET: "Vercel"
  DATABASE_TYPE: "PostgreSQL"
  ORM: "Prisma"
  
options:
  verbose: true
  setup_git: true
```

### Vue.js Progressive Web App

```yaml
# configs/vue-pwa.yml
project:
  name: "vue-pwa-starter"
  description: "Vue.js Progressive Web Application"
  type: "progressive-web-app"
  framework: "vuejs"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["vue", "pwa", "progressive-web-app", "javascript"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Progressive Web Application"
  TECH_STACK: "Vue.js 3, Composition API, PWA, Service Workers"
  NODE_VERSION: "16"
  DEPLOYMENT_TARGET: "Netlify"
  PWA_FEATURES: "Offline Support, Push Notifications, App Install"
```

## 📊 Data Science Projects

### Machine Learning Research Project

```yaml
# configs/ml-research-project.yml
project:
  name: "ml-research-template"
  description: "Machine Learning research project template"
  type: "machine-learning"
  framework: "python-ml"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["machine-learning", "research", "python", "jupyter"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Machine Learning Research"
  TECH_STACK: "Python, Jupyter, PyTorch, Pandas, NumPy"
  PYTHON_VERSION: "3.9"
  ML_FRAMEWORK: "PyTorch"
  DATA_SOURCE: "Custom Dataset"
  RESEARCH_AREA: "Computer Vision"
  
options:
  verbose: true
  create_structure: true
```

### Data Analysis Pipeline

```yaml
# configs/data-analysis-pipeline.yml
project:
  name: "data-analysis-pipeline"
  description: "Automated data analysis and reporting pipeline"
  type: "data-pipeline"
  framework: "python-data"

github:
  enabled: true
  create_repo: true
  private: true
  branch_protection: true
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Data Analysis Pipeline"
  TECH_STACK: "Python, Pandas, Airflow, Docker, AWS"
  PYTHON_VERSION: "3.8"
  DATA_SOURCES: "API, Database, CSV Files"
  ORCHESTRATION: "Apache Airflow"
  DEPLOYMENT_TARGET: "AWS ECS"
  
options:
  verbose: true
  setup_git: true
  install_dependencies: false
```

### Jupyter Notebook Collection

```yaml
# configs/jupyter-notebooks.yml
project:
  name: "data-science-notebooks"
  description: "Collection of data science notebooks and experiments"
  type: "jupyter-notebooks"
  framework: "jupyter"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["jupyter", "data-science", "notebooks", "python"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Data Science Notebooks"
  TECH_STACK: "Jupyter, Python, Pandas, Matplotlib, Seaborn"
  PYTHON_VERSION: "3.9"
  NOTEBOOK_TOPICS: "EDA, Visualization, Statistical Analysis"
  
options:
  verbose: true
  backup_existing: true
```

## 🏢 Enterprise Applications

### Microservice Application

```yaml
# configs/enterprise-microservice.yml
project:
  name: "enterprise-microservice"
  description: "Enterprise-grade microservice application"
  type: "microservice"
  framework: "spring-boot"

github:
  enabled: true
  create_repo: true
  private: true
  organization: "enterprise-org"
  branch_protection: true
  
  branch_protection:
    required_reviews: 2
    require_code_owner_reviews: true
    dismiss_stale_reviews: true
    required_status_checks:
      - "ci/build"
      - "ci/test"
      - "security/scan"
      - "quality/sonarqube"
    restrict_pushes: true
    
  teams:
    - name: "backend-team"
      permission: "push"
    - name: "senior-developers"
      permission: "admin"
    
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Enterprise Microservice"
  TECH_STACK: "Spring Boot, Java 17, Maven, Docker, Kubernetes"
  JAVA_VERSION: "17"
  FRAMEWORK: "Spring Boot 3.0"
  DEPLOYMENT_TARGET: "Kubernetes"
  MONITORING: "Prometheus, Grafana"
  SECURITY_TIER: "High"
  COMPLIANCE: "SOC2, GDPR"
  
options:
  verbose: true
  setup_git: true
  backup_existing: true
```

### Enterprise Web Portal

```yaml
# configs/enterprise-web-portal.yml
project:
  name: "enterprise-portal"
  description: "Enterprise web portal with SSO and role-based access"
  type: "enterprise-web-portal"
  framework: "angular"

github:
  enabled: true
  create_repo: true
  private: true
  organization: "company-name"
  branch_protection: true
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Enterprise Web Portal"
  TECH_STACK: "Angular, TypeScript, .NET Core, Azure AD"
  NODE_VERSION: "18"
  DOTNET_VERSION: "7.0"
  AUTHENTICATION: "Azure Active Directory"
  AUTHORIZATION: "Role-Based Access Control"
  DEPLOYMENT_TARGET: "Azure App Service"
  SECURITY_FEATURES: "SSO, MFA, RBAC"
  
options:
  verbose: false
  setup_git: true
```

## 🔧 API and Backend Services

### REST API Service

```yaml
# configs/rest-api-service.yml
project:
  name: "rest-api-service"
  description: "RESTful API service with authentication and documentation"
  type: "api-service"
  framework: "fastapi"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["api", "rest", "fastapi", "python", "backend"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "REST API Service"
  TECH_STACK: "FastAPI, Python, PostgreSQL, Docker"
  PYTHON_VERSION: "3.9"
  FRAMEWORK: "FastAPI"
  DATABASE: "PostgreSQL"
  AUTHENTICATION: "JWT Bearer Tokens"
  DOCUMENTATION: "OpenAPI/Swagger"
  DEPLOYMENT_TARGET: "Docker Container"
  
options:
  verbose: true
  create_structure: true
```

### GraphQL API Service

```yaml
# configs/graphql-api.yml
project:
  name: "graphql-api-service"
  description: "GraphQL API service with real-time subscriptions"
  type: "graphql-api"
  framework: "apollo-server"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["graphql", "apollo", "nodejs", "api", "backend"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "GraphQL API Service"
  TECH_STACK: "Apollo Server, Node.js, TypeScript, MongoDB"
  NODE_VERSION: "18"
  FRAMEWORK: "Apollo Server"
  DATABASE: "MongoDB"
  FEATURES: "Subscriptions, DataLoader, Schema Stitching"
  DEPLOYMENT_TARGET: "AWS Lambda"
  
options:
  verbose: true
  setup_git: true
```

## 🛠️ Development Tools and Utilities

### CLI Tool

```yaml
# configs/cli-tool.yml
project:
  name: "awesome-cli-tool"
  description: "Command-line interface tool with rich features"
  type: "cli-tool"
  framework: "click"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["cli", "tool", "python", "command-line"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Command-Line Tool"
  TECH_STACK: "Python, Click, Rich, Typer"
  PYTHON_VERSION: "3.8"
  CLI_FRAMEWORK: "Click"
  PACKAGING: "PyPI"
  DOCUMENTATION: "Sphinx"
  
options:
  verbose: true
  create_structure: true
```

### Development Library

```yaml
# configs/python-library.yml
project:
  name: "python-utility-library"
  description: "Reusable Python library with comprehensive testing"
  type: "library"
  framework: "python-lib"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["library", "python", "utilities", "open-source"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Python Library"
  TECH_STACK: "Python, pytest, Sphinx, setuptools"
  PYTHON_VERSION: "3.8"
  TESTING_FRAMEWORK: "pytest"
  DOCUMENTATION: "Sphinx"
  PACKAGING: "PyPI"
  LICENSE_TYPE: "MIT"
  
options:
  verbose: true
  create_structure: true
  setup_git: true
```

## 🏗️ Infrastructure and DevOps

### Terraform Infrastructure

```yaml
# configs/terraform-infrastructure.yml
project:
  name: "terraform-aws-infrastructure"
  description: "AWS infrastructure management with Terraform"
  type: "infrastructure"
  framework: "terraform"

github:
  enabled: true
  create_repo: true
  private: true
  branch_protection: true
  
  branch_protection:
    required_reviews: 1
    required_status_checks:
      - "terraform/validate"
      - "terraform/plan"
      - "security/tfsec"
    
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Infrastructure as Code"
  TECH_STACK: "Terraform, AWS, GitHub Actions"
  TERRAFORM_VERSION: "1.3"
  CLOUD_PROVIDER: "AWS"
  SECURITY_SCANNING: "tfsec, checkov"
  DEPLOYMENT_STRATEGY: "Blue-Green"
  
options:
  verbose: true
  setup_git: true
```

### Docker Application

```yaml
# configs/docker-application.yml
project:
  name: "dockerized-application"
  description: "Containerized application with multi-stage builds"
  type: "docker-application"
  framework: "docker"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["docker", "containerization", "microservice"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Containerized Application"
  TECH_STACK: "Docker, Multi-stage builds, Health checks"
  BASE_IMAGE: "alpine:latest"
  CONTAINER_REGISTRY: "Docker Hub"
  ORCHESTRATION: "Docker Compose"
  
options:
  verbose: true
  create_structure: true
```

## 📱 Mobile Applications

### React Native App

```yaml
# configs/react-native-app.yml
project:
  name: "react-native-mobile-app"
  description: "Cross-platform mobile application with React Native"
  type: "mobile-application"
  framework: "react-native"

github:
  enabled: true
  create_repo: true
  private: true
  topics: ["react-native", "mobile", "ios", "android"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Mobile Application"
  TECH_STACK: "React Native, TypeScript, Expo"
  NODE_VERSION: "18"
  PLATFORMS: "iOS, Android"
  DEPLOYMENT: "App Store, Google Play"
  NAVIGATION: "React Navigation"
  
options:
  verbose: true
  setup_git: true
```

## 🎓 Educational Projects

### Tutorial Series

```yaml
# configs/tutorial-series.yml
project:
  name: "web-development-tutorial"
  description: "Step-by-step web development tutorial series"
  type: "educational"
  framework: "tutorial"

github:
  enabled: true
  create_repo: true
  private: false
  topics: ["tutorial", "education", "web-development", "learning"]
  
templates:
  enabled_templates:
    - "gitignore"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Educational Tutorial"
  SUBJECT_AREA: "Web Development"
  TARGET_AUDIENCE: "Beginners to Intermediate"
  TECH_STACK: "HTML, CSS, JavaScript, Node.js"
  TUTORIAL_FORMAT: "Step-by-step guide with examples"
  
options:
  verbose: true
  backup_existing: true
```

## 🔧 Using Configuration Examples

### Loading Examples

```bash
# Use a specific configuration example
python seeding.py --config ./configs/react-typescript-app.yml

# Override specific settings
python seeding.py --config ./configs/react-typescript-app.yml --project-name "my-custom-app"

# Combine multiple configurations
python seeding.py --config ./configs/base.yml --config ./configs/react-overrides.yml
```

### Customizing Examples

```yaml
# Start with an example and customize
inherit_from: "./examples/react-typescript-app.yml"

# Override specific settings
project:
  name: "my-custom-react-app"
  description: "My customized React application"

variables:
  ADDITIONAL_FEATURES: "PWA, Offline Support"
  CUSTOM_STYLING: "Styled Components"
```

### Creating Your Own Templates

```bash
# Save current configuration as template
python seeding.py --save-config ./my-templates/custom-template.yml --dry-run

# Use your custom template
python seeding.py --config ./my-templates/custom-template.yml
```

---

*For more information on configuration options, see the [Configuration Guide](../guides/configuration.md) and [CLI Reference](../reference/cli.md).*