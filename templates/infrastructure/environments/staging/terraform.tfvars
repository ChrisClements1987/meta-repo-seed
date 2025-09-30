# {{PROJECT_NAME}} Staging Environment Configuration
# Terraform variables for staging deployment
# Production-like settings for testing and validation

# Project Configuration
project_name = "{{PROJECT_NAME}}"
environment  = "staging"
region       = "us-east-1"

# Network Configuration
vpc_cidr = "10.1.0.0/16"
availability_zones = [
  "us-east-1a",
  "us-east-1b",
  "us-east-1c"
]

public_subnet_cidrs = [
  "10.1.1.0/24",
  "10.1.2.0/24",
  "10.1.3.0/24"
]

private_subnet_cidrs = [
  "10.1.10.0/24",
  "10.1.11.0/24",
  "10.1.12.0/24"
]

# Compute Configuration
instance_type = "t3.small"
min_size      = 1
max_size      = 4
desired_capacity = 2

# Database Configuration
db_instance_class    = "db.t3.small"
db_allocated_storage = 50
db_max_allocated_storage = 100
db_engine_version    = "8.0"
db_backup_retention_period = 7
db_backup_window    = "03:00-04:00"
db_maintenance_window = "sun:04:00-sun:05:00"
db_multi_az         = true
db_storage_encrypted = true
db_deletion_protection = false

# Cache Configuration
redis_node_type = "cache.t3.small"
redis_num_cache_nodes = 2
redis_parameter_group_name = "default.redis7"
redis_engine_version = "7.0"
redis_port = 6379

# Security Configuration
enable_deletion_protection = false
enable_backup_encryption  = true
enable_logging           = true
enable_monitoring        = true

# SSL/TLS Configuration
ssl_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/staging-cert-id"

# Domain Configuration
domain_name = "{{PROJECT_NAME}}-staging.com"
create_route53_records = true

# Monitoring Configuration
enable_cloudwatch_alarms = true
enable_detailed_monitoring = true
log_retention_days = 14

# Cost Optimization
enable_spot_instances = false
spot_price = ""

# Backup Configuration
backup_schedule = "0 2 * * *"  # Daily at 2 AM
backup_retention_days = 14

# Auto Scaling Configuration
scale_up_threshold = 70
scale_down_threshold = 30
scale_up_adjustment = 1
scale_down_adjustment = -1

# Load Balancer Configuration
lb_idle_timeout = 120
lb_connection_draining_timeout = 300
lb_cross_zone_load_balancing = true

# Security Groups
allowed_cidr_blocks = [
  "10.1.0.0/16",    # Staging VPC CIDR
  "10.0.0.0/16",    # Dev VPC CIDR (for testing)
]

# Enable/Disable Features
enable_nat_gateway = true
enable_vpn_gateway = false
enable_flow_logs   = true
enable_config      = true
enable_cloudtrail  = true

# Resource Tags
tags = {
  Environment        = "staging"
  Project           = "{{PROJECT_NAME}}"
  Owner             = "{{GITHUB_USERNAME}}"
  CostCenter        = "staging"
  Backup            = "required"
  Monitoring        = "enhanced"
  CreatedBy         = "terraform"
  ManagedBy         = "{{GITHUB_USERNAME}}"
  Purpose           = "staging-validation"
  DataClassification = "internal"
  Compliance        = "soc2"
}

# Staging-specific settings
enable_debug_logging = false
enable_development_tools = false
skip_final_snapshot = false

# Container Configuration
container_cpu    = 512
container_memory = 1024
container_port   = 8000

# ECS Configuration (if using ECS)
ecs_cluster_name = "{{PROJECT_NAME}}-staging-cluster"
ecs_service_desired_count = 2
ecs_task_cpu = 512
ecs_task_memory = 1024

# Lambda Configuration (if using Lambda)
lambda_runtime = "nodejs18.x"
lambda_timeout = 60
lambda_memory_size = 256

# API Gateway Configuration (if using API Gateway)
api_gateway_stage = "staging"
api_gateway_throttle_rate_limit = 5000
api_gateway_throttle_burst_limit = 10000

# CloudFront Configuration (if using CloudFront)
cloudfront_price_class = "PriceClass_200"
cloudfront_enable_compression = true
cloudfront_default_ttl = 3600

# ElastiCache Configuration
elasticache_engine = "redis"
elasticache_node_type = "cache.t3.small"
elasticache_num_cache_nodes = 2
elasticache_port = 6379

# S3 Configuration
s3_versioning_enabled = true
s3_lifecycle_enabled = true
s3_transition_to_ia_days = 30
s3_transition_to_glacier_days = 90
s3_expiration_days = 730

# SNS Configuration
sns_email_endpoint = "staging-alerts@{{PROJECT_NAME}}.com"

# SQS Configuration
sqs_visibility_timeout_seconds = 300
sqs_message_retention_seconds = 1209600
sqs_delay_seconds = 0

# Staging Access
staging_access_cidrs = [
  "203.0.113.0/24",  # Office network
  "198.51.100.0/24", # VPN network
]

# Database Staging Settings
db_publicly_accessible = false
db_skip_final_snapshot = false
db_copy_tags_to_snapshot = true
db_auto_minor_version_upgrade = true
db_apply_immediately = false

# Performance Insights
db_performance_insights_enabled = true
db_performance_insights_retention_period = 7

# Enhanced Monitoring
db_monitoring_interval = 60
db_monitoring_role_arn = "arn:aws:iam::123456789012:role/rds-monitoring-role"

# Staging Database Options
db_option_group_name = ""
db_parameter_group_name = "{{PROJECT_NAME}}-staging-params"

# Secret Manager Configuration
secrets_recovery_window_in_days = 7

# IAM Configuration
create_iam_roles = true
iam_path = "/{{PROJECT_NAME}}/staging/"

# KMS Configuration
kms_deletion_window_in_days = 10

# WAF Configuration
enable_waf = true
waf_rate_limit = 2000
waf_block_malicious_ips = true

# CloudWatch Configuration
cloudwatch_log_group_retention_in_days = 14
enable_cloudwatch_logs = true
enable_x_ray_tracing = true

# Security Configuration
enable_guard_duty = true
enable_security_hub = true
enable_config_rules = true

# Compliance Configuration
enable_compliance_monitoring = true
compliance_standards = ["SOC2", "PCI-DSS"]

# Disaster Recovery
enable_cross_region_backups = true
backup_region = "us-west-2"

# Notification Configuration
notification_endpoints = [
  "staging-team@{{PROJECT_NAME}}.com",
  "devops@{{PROJECT_NAME}}.com"
]

# SSL/TLS Configuration
ssl_policy = "ELBSecurityPolicy-TLS-1-2-2017-01"
certificate_transparency_logging = true

# Data Retention Policies
log_retention_policy = "14_days"
metric_retention_policy = "30_days"
backup_retention_policy = "14_days"

# Feature Flags for Staging
feature_flags = {
  new_ui_enabled           = true
  beta_features_enabled    = false
  analytics_enabled        = true
  monitoring_enabled       = true
  caching_enabled         = true
  rate_limiting_enabled   = true
  authentication_required = true
}

# Integration Testing Configuration
enable_integration_tests = true
test_data_retention_days = 7

# Performance Testing
enable_load_testing = true
max_concurrent_users = 1000

# Security Testing
enable_security_scanning = true
vulnerability_scanning_schedule = "0 6 * * *"  # Daily at 6 AM

# Blue-Green Deployment
enable_blue_green_deployment = true
deployment_strategy = "blue_green"

# Staging Specific Variables
staging_mode = true
debug_enabled = false
verbose_logging = false
mock_external_services = false
disable_authentication = false
enable_cors = true
cors_allowed_origins = [
  "https://{{PROJECT_NAME}}-staging.com",
  "https://www.{{PROJECT_NAME}}-staging.com"
]

# Third-party Integrations
enable_datadog_integration = true
enable_newrelic_integration = false
enable_sentry_integration = true

# Content Delivery Network
enable_cdn = true
cdn_regions = ["us", "eu"]

# Database Read Replicas
enable_read_replicas = true
read_replica_count = 1
read_replica_instance_class = "db.t3.small"

# Elasticsearch Configuration (if using)
elasticsearch_version = "7.10"
elasticsearch_instance_type = "t3.small.elasticsearch"
elasticsearch_instance_count = 2

# Queue Configuration
enable_message_queuing = true
queue_visibility_timeout = 300
dead_letter_queue_enabled = true
