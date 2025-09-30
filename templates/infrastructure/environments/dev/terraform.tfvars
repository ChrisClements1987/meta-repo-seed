# {{PROJECT_NAME}} Development Environment Configuration
# Terraform variables for development deployment
# Cost-optimized settings for development and testing

# Project Configuration
project_name = "{{PROJECT_NAME}}"
environment  = "dev"
region       = "us-east-1"

# Network Configuration
vpc_cidr = "10.0.0.0/16"
availability_zones = [
  "us-east-1a",
  "us-east-1b"
]

public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]

private_subnet_cidrs = [
  "10.0.10.0/24",
  "10.0.11.0/24"
]

# Compute Configuration
instance_type = "t3.micro"
min_size      = 1
max_size      = 2
desired_capacity = 1

# Database Configuration
db_instance_class    = "db.t3.micro"
db_allocated_storage = 20
db_engine_version    = "8.0"
db_backup_retention_period = 1
db_backup_window    = "03:00-04:00"
db_maintenance_window = "sun:04:00-sun:05:00"
db_multi_az         = false
db_storage_encrypted = true
db_deletion_protection = false

# Cache Configuration
redis_node_type = "cache.t3.micro"
redis_num_cache_nodes = 1
redis_parameter_group_name = "default.redis7"
redis_engine_version = "7.0"
redis_port = 6379

# Security Configuration
enable_deletion_protection = false
enable_backup_encryption  = true
enable_logging           = true
enable_monitoring        = true

# SSL/TLS Configuration
ssl_certificate_arn = ""  # Leave empty for development, will use self-signed

# Domain Configuration
domain_name = "{{PROJECT_NAME}}-dev.local"
create_route53_records = false

# Monitoring Configuration
enable_cloudwatch_alarms = true
enable_detailed_monitoring = false
log_retention_days = 7

# Cost Optimization
enable_spot_instances = true
spot_price = "0.05"

# Backup Configuration
backup_schedule = "0 2 * * *"  # Daily at 2 AM
backup_retention_days = 7

# Auto Scaling Configuration
scale_up_threshold = 80
scale_down_threshold = 20
scale_up_adjustment = 1
scale_down_adjustment = -1

# Load Balancer Configuration
lb_idle_timeout = 60
lb_connection_draining_timeout = 60
lb_cross_zone_load_balancing = true

# Security Groups
allowed_cidr_blocks = [
  "10.0.0.0/16",    # VPC CIDR
  "172.16.0.0/12",  # Private networks
  "192.168.0.0/16"  # Private networks
]

# Enable/Disable Features
enable_nat_gateway = true
enable_vpn_gateway = false
enable_flow_logs   = false
enable_config      = false
enable_cloudtrail  = false

# Resource Tags
tags = {
  Environment        = "dev"
  Project           = "{{PROJECT_NAME}}"
  Owner             = "{{GITHUB_USERNAME}}"
  CostCenter        = "development"
  Backup            = "required"
  Monitoring        = "basic"
  CreatedBy         = "terraform"
  ManagedBy         = "{{GITHUB_USERNAME}}"
  Purpose           = "development-testing"
  DataClassification = "internal"
  Compliance        = "none"
}

# Development-specific settings
enable_debug_logging = true
enable_development_tools = true
skip_final_snapshot = true

# Container Configuration
container_cpu    = 256
container_memory = 512
container_port   = 8000

# ECS Configuration (if using ECS)
ecs_cluster_name = "{{PROJECT_NAME}}-dev-cluster"
ecs_service_desired_count = 1
ecs_task_cpu = 256
ecs_task_memory = 512

# Lambda Configuration (if using Lambda)
lambda_runtime = "nodejs18.x"
lambda_timeout = 30
lambda_memory_size = 128

# API Gateway Configuration (if using API Gateway)
api_gateway_stage = "dev"
api_gateway_throttle_rate_limit = 1000
api_gateway_throttle_burst_limit = 2000

# CloudFront Configuration (if using CloudFront)
cloudfront_price_class = "PriceClass_100"
cloudfront_enable_compression = true
cloudfront_default_ttl = 86400

# ElastiCache Configuration
elasticache_engine = "redis"
elasticache_node_type = "cache.t3.micro"
elasticache_num_cache_nodes = 1
elasticache_port = 6379

# S3 Configuration
s3_versioning_enabled = false
s3_lifecycle_enabled = true
s3_transition_to_ia_days = 30
s3_transition_to_glacier_days = 90
s3_expiration_days = 365

# SNS Configuration
sns_email_endpoint = "{{GITHUB_USERNAME}}@example.com"

# SQS Configuration
sqs_visibility_timeout_seconds = 300
sqs_message_retention_seconds = 345600
sqs_delay_seconds = 0

# Development Access
development_access_cidrs = [
  "0.0.0.0/0"  # Allow from anywhere for development
]

# Database Development Settings
db_publicly_accessible = false
db_skip_final_snapshot = true
db_copy_tags_to_snapshot = false
db_auto_minor_version_upgrade = true
db_apply_immediately = true

# Performance Insights
db_performance_insights_enabled = false
db_performance_insights_retention_period = 7

# Enhanced Monitoring
db_monitoring_interval = 0
db_monitoring_role_arn = ""

# Development Database Options
db_option_group_name = ""
db_parameter_group_name = ""

# Secret Manager Configuration
secrets_recovery_window_in_days = 0  # Immediate deletion for dev

# IAM Configuration
create_iam_roles = true
iam_path = "/{{PROJECT_NAME}}/dev/"

# KMS Configuration
kms_deletion_window_in_days = 7  # Shorter for dev environment

# Development Specific Variables
development_mode = true
debug_enabled = true
verbose_logging = true
mock_external_services = true
disable_authentication = false
enable_cors = true
cors_allowed_origins = ["*"]

# Feature Flags for Development
feature_flags = {
  new_ui_enabled           = true
  beta_features_enabled    = true
  analytics_enabled        = false
  monitoring_enabled       = true
  caching_enabled         = true
  rate_limiting_enabled   = false
  authentication_required = true
}

# Development Tools
enable_adminer = true
enable_mailhog = true
enable_redis_commander = true
enable_prometheus = false
enable_grafana = false
