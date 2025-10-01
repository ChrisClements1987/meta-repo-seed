#!/bin/bash
# {{PROJECT_NAME}} Infrastructure Deployment Orchestration Script
# Enables true 10-minute deployment for Business-in-a-Box vision
# Integrates Infrastructure as Code with Business Operations Automation

set -euo pipefail

# Configuration
PROJECT_NAME="{{PROJECT_NAME}}"
GITHUB_USERNAME="{{GITHUB_USERNAME}}"
BUSINESS_PROFILE="{{BUSINESS_PROFILE:-startup-basic}}"
ENVIRONMENT="${ENVIRONMENT:-production}"
CLOUD_PROVIDER="${CLOUD_PROVIDER:-aws}"
DRY_RUN="${DRY_RUN:-false}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
print_banner() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "🚀 ${PROJECT_NAME} Infrastructure Deployment"
    echo "=================================================="
    echo "Business Profile: ${BUSINESS_PROFILE}"
    echo "Environment: ${ENVIRONMENT}"
    echo "Cloud Provider: ${CLOUD_PROVIDER}"
    echo "Dry Run: ${DRY_RUN}"
    echo "=================================================="
    echo -e "${NC}"
}

# Prerequisites check
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    # Check required tools
    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi
    
    if ! command -v terraform &> /dev/null; then
        missing_tools+=("terraform")
    fi
    
    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi
    
    # Cloud provider specific checks
    case $CLOUD_PROVIDER in
        aws)
            if ! command -v aws &> /dev/null; then
                missing_tools+=("aws-cli")
            fi
            ;;
        azure)
            if ! command -v az &> /dev/null; then
                missing_tools+=("azure-cli")
            fi
            ;;
        gcp)
            if ! command -v gcloud &> /dev/null; then
                missing_tools+=("gcloud")
            fi
            ;;
    esac
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        echo "Please install missing tools before continuing."
        exit 1
    fi
    
    log_success "All prerequisites met!"
}

# Initialize Terraform backend
initialize_terraform_backend() {
    log_info "Initializing Terraform backend..."
    
    cd infrastructure/terraform
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would initialize Terraform backend"
        return 0
    fi
    
    # Initialize Terraform
    terraform init \
        -backend-config="bucket=${PROJECT_NAME}-terraform-state" \
        -backend-config="key=${PROJECT_NAME}/${ENVIRONMENT}/terraform.tfstate" \
        -backend-config="region=us-east-1"
    
    cd ../..
    log_success "Terraform backend initialized!"
}

# Deploy cloud infrastructure
deploy_cloud_infrastructure() {
    log_info "Deploying ${CLOUD_PROVIDER} infrastructure..."
    
    cd infrastructure/terraform
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would deploy cloud infrastructure"
        terraform plan \
            -var-file="../environments/${ENVIRONMENT}/terraform.tfvars" \
            -var="business_profile=${BUSINESS_PROFILE}"
        cd ../..
        return 0
    fi
    
    # Plan deployment
    terraform plan \
        -var-file="../environments/${ENVIRONMENT}/terraform.tfvars" \
        -var="business_profile=${BUSINESS_PROFILE}" \
        -out=tfplan
    
    # Apply deployment
    log_info "Applying Terraform plan..."
    terraform apply tfplan
    
    cd ../..
    log_success "Cloud infrastructure deployed!"
}

# Deploy Kubernetes resources
deploy_kubernetes_resources() {
    log_info "Deploying Kubernetes resources..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would deploy Kubernetes resources"
        kubectl apply --dry-run=client -f infrastructure/kubernetes/
        return 0
    fi
    
    # Apply Kubernetes manifests
    kubectl apply -f infrastructure/kubernetes/namespace.yaml
    kubectl apply -f infrastructure/kubernetes/configmap.yaml
    kubectl apply -f infrastructure/kubernetes/secret.yaml
    kubectl apply -f infrastructure/kubernetes/deployment.yaml
    kubectl apply -f infrastructure/kubernetes/service.yaml
    kubectl apply -f infrastructure/kubernetes/ingress.yaml
    
    log_success "Kubernetes resources deployed!"
}

# Deploy monitoring stack
deploy_monitoring_stack() {
    log_info "Deploying monitoring stack..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would deploy monitoring stack"
        return 0
    fi
    
    # Deploy Prometheus
    if [ -f "infrastructure/monitoring/prometheus.yml" ]; then
        kubectl create configmap prometheus-config \
            --from-file=infrastructure/monitoring/prometheus.yml \
            --dry-run=client -o yaml | kubectl apply -f -
    fi
    
    # Deploy Grafana dashboards
    if [ -f "infrastructure/monitoring/grafana-dashboard-business-operations.json" ]; then
        kubectl create configmap grafana-dashboard-business-ops \
            --from-file=infrastructure/monitoring/grafana-dashboard-business-operations.json \
            --dry-run=client -o yaml | kubectl apply -f -
    fi
    
    log_success "Monitoring stack deployed!"
}

# Setup business operations automation
setup_business_operations() {
    log_info "Setting up business operations automation..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would setup business operations automation"
        return 0
    fi
    
    # Deploy business operations workflows
    if [ -d ".github/workflows" ]; then
        log_info "Business operations workflows already configured via GitHub Actions"
    fi
    
    # Create business profile configuration
    cat > governance/business-profile.yml << EOF
profile: ${BUSINESS_PROFILE}
environment: ${ENVIRONMENT}
organization: ${GITHUB_USERNAME}
repository: ${PROJECT_NAME}
automation_level: standard
self_healing_enabled: true
compliance_enforcement: true
automated_reporting: true
created_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
managed_by: business-operations-automation
EOF
    
    log_success "Business operations automation configured!"
}

# Build and deploy application
build_and_deploy_application() {
    log_info "Building and deploying application..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would build and deploy application"
        return 0
    fi
    
    # Build Docker image
    if [ -f "infrastructure/docker/Dockerfile.template" ]; then
        # Copy and process Dockerfile template
        sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g; s/{{GITHUB_USERNAME}}/${GITHUB_USERNAME}/g" \
            infrastructure/docker/Dockerfile.template > Dockerfile
        
        docker build -t "${GITHUB_USERNAME}/${PROJECT_NAME}:${ENVIRONMENT}" .
        
        # Push to registry if not local deployment
        if [ "$ENVIRONMENT" != "dev" ]; then
            docker push "${GITHUB_USERNAME}/${PROJECT_NAME}:${ENVIRONMENT}"
        fi
    fi
    
    log_success "Application built and deployed!"
}

# Health checks
perform_health_checks() {
    log_info "Performing health checks..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would perform health checks"
        return 0
    fi
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        log_info "Health check attempt $attempt/$max_attempts"
        
        # Check Kubernetes pods
        if kubectl get pods -l app="${PROJECT_NAME}" --field-selector=status.phase=Running | grep -q "${PROJECT_NAME}"; then
            log_success "Application pods are running!"
            break
        fi
        
        if [ $attempt -eq $max_attempts ]; then
            log_error "Health checks failed after $max_attempts attempts"
            return 1
        fi
        
        sleep 10
        ((attempt++))
    done
    
    log_success "All health checks passed!"
}

# Generate deployment report
generate_deployment_report() {
    log_info "Generating deployment report..."
    
    local report_file="deployment-report-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$report_file" << EOF
# ${PROJECT_NAME} Infrastructure Deployment Report

**Date:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Business Profile:** ${BUSINESS_PROFILE}
**Environment:** ${ENVIRONMENT}
**Cloud Provider:** ${CLOUD_PROVIDER}

## Deployment Summary

- ✅ Cloud Infrastructure: Deployed
- ✅ Kubernetes Resources: Deployed
- ✅ Monitoring Stack: Deployed
- ✅ Business Operations: Configured
- ✅ Application: Built and Deployed
- ✅ Health Checks: Passed

## Resources Created

### Infrastructure
$(if [ "$DRY_RUN" != "true" ]; then cd infrastructure/terraform && terraform output && cd ../..; else echo "DRY RUN - No actual resources created"; fi)

### Kubernetes
- Namespace: ${PROJECT_NAME}
- Deployments: ${PROJECT_NAME}-app
- Services: ${PROJECT_NAME}-service
- Ingress: ${PROJECT_NAME}-ingress

### Monitoring
- Prometheus: Configured
- Grafana: Business Operations Dashboard
- Alerts: Business Profile Specific

## Business Operations Automation

- **Profile:** ${BUSINESS_PROFILE}
- **Self-Healing:** Enabled
- **Compliance Enforcement:** Enabled
- **Automated Reporting:** Enabled

## Next Steps

1. Verify application accessibility via ingress URL
2. Check business operations dashboard
3. Review automated workflow execution
4. Schedule first compliance review

## Support

For issues or questions:
- Repository: https://github.com/${GITHUB_USERNAME}/${PROJECT_NAME}
- Business Operations: Check governance/business-profile.yml
- Monitoring: Access Grafana dashboard

---
*Report generated by ${PROJECT_NAME} Infrastructure Deployment System*
EOF

    if [ "$DRY_RUN" != "true" ]; then
        mkdir -p reports/infrastructure
        mv "$report_file" "reports/infrastructure/"
        log_success "Deployment report saved to reports/infrastructure/$report_file"
    else
        log_info "DRY RUN: Deployment report generated (not saved)"
        rm "$report_file"
    fi
}

# Rollback function
rollback_deployment() {
    log_warning "Rolling back deployment..."
    
    if [ "$DRY_RUN" = "true" ]; then
        log_info "DRY RUN: Would rollback deployment"
        return 0
    fi
    
    # Rollback Kubernetes resources
    kubectl delete -f infrastructure/kubernetes/ --ignore-not-found=true
    
    # Rollback Terraform (if needed)
    cd infrastructure/terraform
    terraform destroy -auto-approve \
        -var-file="../environments/${ENVIRONMENT}/terraform.tfvars" \
        -var="business_profile=${BUSINESS_PROFILE}"
    cd ../..
    
    log_warning "Deployment rolled back!"
}

# Cleanup function
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deployment failed with exit code $exit_code"
        if [ "$ENVIRONMENT" = "production" ]; then
            log_warning "Production deployment failed - manual intervention required"
        else
            rollback_deployment
        fi
    fi
    exit $exit_code
}

# Main deployment flow
main() {
    print_banner
    
    # Set trap for cleanup
    trap cleanup EXIT
    
    # Deployment steps
    check_prerequisites
    initialize_terraform_backend
    deploy_cloud_infrastructure
    deploy_kubernetes_resources
    deploy_monitoring_stack
    setup_business_operations
    build_and_deploy_application
    perform_health_checks
    generate_deployment_report
    
    log_success "🎉 ${PROJECT_NAME} infrastructure deployment completed successfully!"
    log_info "🕒 Total deployment time: approximately $(date)"
    log_info "📊 Access your business operations dashboard via Grafana"
    log_info "🔧 Business automation workflows are now active"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        log_info "🚀 Production deployment complete - Business-in-a-Box is live!"
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
