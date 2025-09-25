"""
Product Template Generator

Generates production-ready applications from templates with:
- Complete application scaffolding
- CI/CD pipeline configuration
- PaaS deployment configuration
- Environment-specific settings
- Professional documentation
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime

# Add the root directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from seeding import setup_logging


@dataclass
class TemplateConfig:
    """Configuration for a product template."""
    name: str
    display_name: str
    description: str
    technologies: List[str]
    deployment_target: str
    features: List[str]
    template_dir: str
    build_command: Optional[str] = None
    start_command: Optional[str] = None
    output_directory: Optional[str] = None
    environment_variables: List[str] = None
    
    def __post_init__(self):
        if self.environment_variables is None:
            self.environment_variables = []


class ProductTemplateRegistry:
    """Registry of all available product templates."""
    
    TEMPLATES = {
        'nextjs': TemplateConfig(
            name='nextjs',
            display_name='Next.js Application',
            description='Full-stack React application with SSR/SSG, API routes, and modern tooling',
            technologies=['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'Prisma'],
            deployment_target='vercel',
            features=[
                'Server-side rendering (SSR)',
                'Static site generation (SSG)',
                'API routes with serverless functions',
                'TypeScript with strict configuration',
                'Tailwind CSS for styling',
                'Prisma ORM ready',
                'Authentication setup (NextAuth.js)',
                'ESLint and Prettier configured',
                'Testing setup (Jest + Testing Library)',
                'SEO optimization'
            ],
            template_dir='nextjs-app',
            build_command='npm run build',
            start_command='npm start',
            output_directory='.next',
            environment_variables=[
                'DATABASE_URL',
                'NEXTAUTH_SECRET',
                'NEXTAUTH_URL'
            ]
        ),
        
        'python-api': TemplateConfig(
            name='python-api',
            display_name='Python FastAPI',
            description='High-performance REST API with async support, automatic docs, and database integration',
            technologies=['Python', 'FastAPI', 'PostgreSQL', 'SQLAlchemy', 'Pydantic'],
            deployment_target='fly.io',
            features=[
                'FastAPI with automatic OpenAPI docs',
                'Async/await support throughout',
                'SQLAlchemy ORM with Alembic migrations',
                'Pydantic data validation',
                'JWT authentication',
                'CORS middleware',
                'Docker containerization',
                'Health check endpoints',
                'Structured logging',
                'pytest testing setup'
            ],
            template_dir='python-fastapi',
            build_command='pip install -r requirements.txt',
            start_command='uvicorn main:app --host 0.0.0.0 --port 8000',
            environment_variables=[
                'DATABASE_URL',
                'SECRET_KEY',
                'ENVIRONMENT'
            ]
        ),
        
        'node-api': TemplateConfig(
            name='node-api',
            display_name='Node.js Express API',
            description='Express.js REST API with TypeScript, middleware, and database integration',
            technologies=['Node.js', 'Express.js', 'TypeScript', 'PostgreSQL', 'Prisma'],
            deployment_target='fly.io',
            features=[
                'Express.js with TypeScript',
                'Prisma ORM with type safety',
                'JWT authentication middleware',
                'Request validation with Joi',
                'CORS and security middleware',
                'Structured logging with Winston',
                'Health check and metrics endpoints',
                'Docker containerization',
                'Jest testing framework',
                'API documentation with Swagger'
            ],
            template_dir='node-express-api',
            build_command='npm run build',
            start_command='npm start',
            output_directory='dist',
            environment_variables=[
                'DATABASE_URL',
                'JWT_SECRET',
                'NODE_ENV',
                'PORT'
            ]
        ),
        
        'react-spa': TemplateConfig(
            name='react-spa',
            display_name='React Single Page Application',
            description='Modern React SPA with routing, state management, and build optimization',
            technologies=['React', 'TypeScript', 'React Router', 'Zustand', 'Vite'],
            deployment_target='netlify',
            features=[
                'React 18+ with modern hooks',
                'TypeScript for type safety',
                'React Router for client-side routing',
                'Zustand for state management',
                'Vite for fast development and building',
                'Tailwind CSS for styling',
                'React Query for server state',
                'Authentication context setup',
                'PWA capabilities',
                'Testing with Vitest and Testing Library'
            ],
            template_dir='react-spa',
            build_command='npm run build',
            start_command='npm run preview',
            output_directory='dist',
            environment_variables=[
                'VITE_API_URL',
                'VITE_AUTH_DOMAIN'
            ]
        ),
        
        'static-site': TemplateConfig(
            name='static-site',
            display_name='Static Website',
            description='Modern static website with build tools, optimization, and deployment',
            technologies=['HTML5', 'CSS3', 'JavaScript', 'Vite', 'Tailwind CSS'],
            deployment_target='cloudflare-pages',
            features=[
                'Modern HTML5 semantic structure',
                'Tailwind CSS for responsive design',
                'Vite for development and building',
                'JavaScript ES6+ modules',
                'Image optimization',
                'SEO meta tags',
                'Performance optimization',
                'Contact form integration',
                'Analytics ready',
                'Lighthouse optimized'
            ],
            template_dir='static-website',
            build_command='npm run build',
            start_command='npm run preview',
            output_directory='dist'
        )
    }
    
    @classmethod
    def get_template(cls, template_name: str) -> Optional[TemplateConfig]:
        """Get template configuration by name."""
        return cls.TEMPLATES.get(template_name)
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List all available template names."""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def get_templates_by_deployment_target(cls, target: str) -> List[TemplateConfig]:
        """Get templates filtered by deployment target."""
        return [template for template in cls.TEMPLATES.values() 
                if template.deployment_target == target]


class ProductTemplateGenerator:
    """Generates production-ready applications from templates."""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template generator.
        
        Args:
            templates_dir: Directory containing template files
        """
        self.logger = logging.getLogger(f"{__name__}.ProductTemplateGenerator")
        
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "product-templates"
        
        self.templates_dir = Path(templates_dir)
        self.logger.debug(f"Template directory: {self.templates_dir}")

    def generate_product(
        self, 
        template_name: str, 
        product_name: str, 
        output_dir: Path,
        variables: Optional[Dict[str, str]] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a product from template.
        
        Args:
            template_name: Name of the template to use
            product_name: Name of the product to create
            output_dir: Directory where product will be created
            variables: Additional template variables
            dry_run: If True, simulate generation without creating files
            
        Returns:
            Dictionary with generation results and configuration
        """
        self.logger.info(f"Generating product: {product_name} from template: {template_name}")
        
        # Get template configuration
        template_config = ProductTemplateRegistry.get_template(template_name)
        if not template_config:
            raise ValueError(f"Unknown template: {template_name}")
        
        # Set up template variables
        template_vars = {
            'PRODUCT_NAME': product_name,
            'PRODUCT_NAME_LOWER': product_name.lower(),
            'PRODUCT_NAME_UPPER': product_name.upper(),
            'PRODUCT_NAME_TITLE': product_name.replace('-', ' ').replace('_', ' ').title(),
            'CURRENT_DATE': datetime.now().strftime('%Y-%m-%d'),
            'CURRENT_YEAR': datetime.now().strftime('%Y'),
            'TEMPLATE_NAME': template_name,
            'DEPLOYMENT_TARGET': template_config.deployment_target
        }
        
        if variables:
            template_vars.update(variables)
        
        # Template source directory
        template_source = self.templates_dir / template_config.template_dir
        product_output_dir = output_dir / product_name
        
        if dry_run:
            self.logger.info("DRY RUN - Would generate product:")
            self.logger.info(f"  Template: {template_config.display_name}")
            self.logger.info(f"  Technologies: {', '.join(template_config.technologies)}")
            self.logger.info(f"  Features: {len(template_config.features)} features")
            self.logger.info(f"  Output: {product_output_dir}")
            self.logger.info(f"  Deployment: {template_config.deployment_target}")
            
            return {
                'success': True,
                'product_name': product_name,
                'template': template_config,
                'output_dir': str(product_output_dir),
                'variables': template_vars,
                'dry_run': True
            }
        
        try:
            # Create output directory
            product_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if template source exists
            if not template_source.exists():
                raise FileNotFoundError(f"Template source not found: {template_source}")
            
            # Copy template files with variable substitution
            self._copy_template_files(template_source, product_output_dir, template_vars)
            
            # Generate CI/CD configuration
            self._generate_cicd_config(product_output_dir, template_config, template_vars)
            
            # Generate deployment configuration
            self._generate_deployment_config(product_output_dir, template_config, template_vars)
            
            # Generate documentation
            self._generate_documentation(product_output_dir, template_config, template_vars)
            
            self.logger.info(f"✓ Product generated successfully: {product_output_dir}")
            
            return {
                'success': True,
                'product_name': product_name,
                'template': template_config,
                'output_dir': str(product_output_dir),
                'variables': template_vars,
                'next_steps': self._get_next_steps(template_config)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate product: {e}")
            return {
                'success': False,
                'error': str(e),
                'product_name': product_name,
                'template': template_config
            }

    def _copy_template_files(self, source: Path, dest: Path, variables: Dict[str, str]):
        """Copy template files with variable substitution."""
        self.logger.debug(f"Copying template files from {source} to {dest}")
        
        for item in source.rglob('*'):
            if item.is_file():
                # Calculate relative path and substitute variables in path
                rel_path = item.relative_to(source)
                dest_path = dest / self._substitute_variables(str(rel_path), variables)
                
                # Create parent directories
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file with variable substitution if it's a text file
                if self._is_text_file(item):
                    content = item.read_text(encoding='utf-8')
                    substituted_content = self._substitute_variables(content, variables)
                    dest_path.write_text(substituted_content, encoding='utf-8')
                else:
                    # Copy binary file as-is
                    shutil.copy2(item, dest_path)

    def _substitute_variables(self, content: str, variables: Dict[str, str]) -> str:
        """Substitute template variables in content."""
        for var_name, var_value in variables.items():
            content = content.replace(f'{{{{{var_name}}}}}', var_value)
        return content

    def _is_text_file(self, path: Path) -> bool:
        """Check if file is a text file that should have variable substitution."""
        text_extensions = {
            '.js', '.ts', '.jsx', '.tsx', '.py', '.html', '.css', '.scss', '.sass',
            '.json', '.yaml', '.yml', '.md', '.txt', '.env', '.gitignore',
            '.dockerignore', '.eslintrc', '.prettierrc', '.toml', '.cfg', '.ini'
        }
        return path.suffix.lower() in text_extensions or path.name.startswith('.')

    def _generate_cicd_config(self, output_dir: Path, template_config: TemplateConfig, variables: Dict[str, str]):
        """Generate CI/CD configuration files."""
        self.logger.debug("Generating CI/CD configuration")
        
        # Create .github/workflows directory
        workflows_dir = output_dir / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate main CI workflow
        ci_workflow = self._generate_ci_workflow(template_config, variables)
        (workflows_dir / 'ci.yml').write_text(ci_workflow, encoding='utf-8')
        
        # Generate deployment workflow if needed
        if template_config.deployment_target:
            deploy_workflow = self._generate_deploy_workflow(template_config, variables)
            (workflows_dir / 'deploy.yml').write_text(deploy_workflow, encoding='utf-8')

    def _generate_ci_workflow(self, template_config: TemplateConfig, variables: Dict[str, str]) -> str:
        """Generate GitHub Actions CI workflow."""
        workflow = f"""name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
      if: contains('{' '.join(template_config.technologies)}', 'Node') || contains('{' '.join(template_config.technologies)}', 'React') || contains('{' '.join(template_config.technologies)}', 'Next')
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
      if: contains('{' '.join(template_config.technologies)}', 'Python')
    
    - name: Install dependencies
      run: |"""
        
        if any('Node' in tech or 'React' in tech or 'Next' in tech for tech in template_config.technologies):
            workflow += "\n        npm ci"
        
        if any('Python' in tech for tech in template_config.technologies):
            workflow += "\n        pip install -r requirements.txt"
            
        workflow += f"""
    
    - name: Run linter
      run: |"""
      
        if any('Node' in tech or 'React' in tech or 'Next' in tech for tech in template_config.technologies):
            workflow += "\n        npm run lint"
        
        if any('Python' in tech for tech in template_config.technologies):
            workflow += "\n        flake8 ."
            
        workflow += f"""
    
    - name: Run tests
      run: |"""
      
        if any('Node' in tech or 'React' in tech or 'Next' in tech for tech in template_config.technologies):
            workflow += "\n        npm test"
        
        if any('Python' in tech for tech in template_config.technologies):
            workflow += "\n        pytest"
            
        workflow += f"""
    
    - name: Build
      run: {template_config.build_command}
      if: steps.changes.outputs.src == 'true'
    
    - name: Security scan
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: security-scan-results.sarif
      continue-on-error: true
"""
        
        return workflow

    def _generate_deploy_workflow(self, template_config: TemplateConfig, variables: Dict[str, str]) -> str:
        """Generate deployment workflow based on target."""
        product_name = variables.get('PRODUCT_NAME', 'app')
        
        if template_config.deployment_target == 'vercel':
            return f"""name: Deploy to Vercel

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: {template_config.build_command}
      env:
        NODE_ENV: production
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{{{ secrets.VERCEL_TOKEN }}}}
        vercel-org-id: ${{{{ secrets.VERCEL_ORG_ID }}}}
        vercel-project-id: ${{{{ secrets.VERCEL_PROJECT_ID }}}}
        working-directory: ./
        vercel-args: '--prod'
"""
        
        elif template_config.deployment_target == 'fly.io':
            return f"""name: Deploy to Fly.io

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    name: Deploy app
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - uses: superfly/flyctl-actions/setup-flyctl@master
    
    - name: Deploy to Fly.io
      run: flyctl deploy --remote-only
      env:
        FLY_API_TOKEN: ${{{{ secrets.FLY_API_TOKEN }}}}
"""
        
        elif template_config.deployment_target == 'netlify':
            return f"""name: Deploy to Netlify

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build
      run: {template_config.build_command}
    
    - name: Deploy to Netlify
      uses: nwtgck/actions-netlify@v2.0
      with:
        publish-dir: './{template_config.output_directory or 'dist'}'
        production-branch: main
        github-token: ${{{{ secrets.GITHUB_TOKEN }}}}
        deploy-message: "Deploy from GitHub Actions"
        enable-pull-request-comment: true
        enable-commit-comment: true
      env:
        NETLIFY_AUTH_TOKEN: ${{{{ secrets.NETLIFY_AUTH_TOKEN }}}}
        NETLIFY_SITE_ID: ${{{{ secrets.NETLIFY_SITE_ID }}}}
"""
        
        return "# Deployment workflow not configured for this target"

    def _generate_deployment_config(self, output_dir: Path, template_config: TemplateConfig, variables: Dict[str, str]):
        """Generate deployment-specific configuration files."""
        if template_config.deployment_target == 'vercel':
            vercel_config = {
                "version": 2,
                "name": variables.get('PRODUCT_NAME'),
                "builds": [
                    {
                        "src": "package.json",
                        "use": "@vercel/next" if 'Next' in template_config.technologies else "@vercel/static-build"
                    }
                ],
                "env": {var: f"@{var.lower()}" for var in template_config.environment_variables}
            }
            (output_dir / 'vercel.json').write_text(json.dumps(vercel_config, indent=2), encoding='utf-8')
        
        elif template_config.deployment_target == 'fly.io':
            fly_config = f"""app = "{variables.get('PRODUCT_NAME_LOWER')}"
kill_signal = "SIGINT"
kill_timeout = 5
processes = []

[env]
  PORT = "8000"
  NODE_ENV = "production"

[experimental]
  auto_rollback = true

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
  [services.concurrency]
    hard_limit = 25
    soft_limit = 20
    type = "connections"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
"""
            (output_dir / 'fly.toml').write_text(fly_config, encoding='utf-8')

    def _generate_documentation(self, output_dir: Path, template_config: TemplateConfig, variables: Dict[str, str]):
        """Generate project documentation."""
        readme_content = f"""# {variables.get('PRODUCT_NAME_TITLE')}

{template_config.description}

## Technologies

{chr(10).join(f'- {tech}' for tech in template_config.technologies)}

## Features

{chr(10).join(f'- {feature}' for feature in template_config.features)}

## Quick Start

1. **Install dependencies**
   ```bash
   {template_config.build_command}
   ```

2. **Start development server**
   ```bash
   {template_config.start_command or 'npm run dev'}
   ```

3. **Build for production**
   ```bash
   {template_config.build_command}
   ```

## Environment Variables

{chr(10).join(f'- `{var}`: [Description needed]' for var in template_config.environment_variables) if template_config.environment_variables else 'No environment variables required.'}

## Deployment

This application is configured for deployment to **{template_config.deployment_target}**.

### Automatic Deployment

Push to the `main` branch triggers automatic deployment via GitHub Actions.

### Manual Deployment

Follow the deployment target specific instructions:

- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **Fly.io**: `flyctl deploy`
- **Cloudflare Pages**: Connected via Git integration

## Project Structure

```
{variables.get('PRODUCT_NAME')}/
├── src/                 # Source code
├── public/              # Static assets
├── .github/workflows/   # CI/CD pipelines
├── package.json         # Dependencies and scripts
└── README.md           # This file
```

## Development

### Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run tests
- `npm run lint` - Run linter

### Code Quality

- ESLint for code linting
- Prettier for code formatting
- TypeScript for type safety
- Testing with Jest/Vitest

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Generated on {variables.get('CURRENT_DATE')} using Business-in-a-Box template system.
"""
        
        (output_dir / 'README.md').write_text(readme_content, encoding='utf-8')

    def _get_next_steps(self, template_config: TemplateConfig) -> List[str]:
        """Get next steps for the generated product."""
        steps = [
            "Install dependencies and start development server",
            "Configure environment variables",
            "Set up database (if required)",
            "Configure deployment secrets in GitHub repository settings",
            "Push code to trigger first deployment",
            "Set up custom domain (optional)"
        ]
        
        if template_config.deployment_target == 'vercel':
            steps.append("Connect Vercel project and configure environment variables")
        elif template_config.deployment_target == 'fly.io':
            steps.append("Create Fly.io app: flyctl apps create your-app-name")
        elif template_config.deployment_target == 'netlify':
            steps.append("Connect Netlify site and configure build settings")
        
        return steps


if __name__ == '__main__':
    # Test the template generator
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    generator = ProductTemplateGenerator()
    
    print("=== Available Product Templates ===")
    for template_name in ProductTemplateRegistry.list_templates():
        template = ProductTemplateRegistry.get_template(template_name)
        print(f"\n{template.display_name} ({template_name})")
        print(f"  Technologies: {', '.join(template.technologies)}")
        print(f"  Deployment: {template.deployment_target}")
        print(f"  Features: {len(template.features)} features")
    
    print("\n=== Test Generation (Dry Run) ===")
    result = generator.generate_product(
        template_name='nextjs',
        product_name='test-webapp',
        output_dir=Path('/tmp'),
        dry_run=True
    )
    
    print(f"Generation result: {'Success' if result['success'] else 'Failed'}")
    if result['success']:
        print(f"Template: {result['template'].display_name}")
        print(f"Output: {result['output_dir']}")
