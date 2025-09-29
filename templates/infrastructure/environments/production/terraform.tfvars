# {{PROJECT_NAME}} Production Environment Configuration
# Terraform variables for production deployment
# High availability, security-hardened configuration

# Project Configuration
project_name = "{{PROJECT_NAME}}"
environment  = "production"
region       = "us-east-1"

# Multi-region Configuration
backup_region = "us-west-2"
enable_multi_region = true

# Network Configuration
vpc_cidr = "10.2.0.0/16"
availability_zones = [
  "us-east-1a",
  "us-east-1b",
  "us-east-1c"
]

public_subnet_cidrs = [
  "10.2.1.0/24",
  "10.2.2.0/24",
  "10.2.3.0/24"
]

private_subnet_cidrs = [
  "10.2.10.0/24",
  "10.2.11.0/24",
  "10.2.12.0/24"
]

database_subnet_cidrs = [
  "10.2.20.0/24",
  "10.2.21.0/24",
  "10.2.22.0/24"
]

# Compute Configuration
instance_type = "m5.large"
min_size      = 3
max_size      = 10
desired_capacity = 5

# Database Configuration
db_instance_class    = "db.r5.xlarge"
db_allocated_storage = 200
db_max_allocated_storage = 1000
db_engine_version    = "8.0"
db_backup_retention_period = 30
db_backup_window    = "03:00-04:00"
db_maintenance_window = "sun:04:00-sun:06:00"
db_multi_az         = true
db_storage_encrypted = true
db_deletion_protection = true

# Cache Configuration
redis_node_type = "cache.r6g.xlarge"
redis_num_cache_clusters = 3
redis_parameter_group_name = "default.redis7.cluster.on"
redis_engine_version = "7.0"
redis_port = 6379
redis_at_rest_encryption_enabled = true
redis_transit_encryption_enabled = true

# Security Configuration
enable_deletion_protection = true
enable_backup_encryption  = true
enable_logging           = true
enable_monitoring        = true

# SSL/TLS Configuration
ssl_certificate_arn = "arn:aws:acm:us-east-1:123456789012:certificate/production-cert-id"
ssl_policy = "ELBSecurityPolicy-TLS-1-2-2017-01"

# Domain Configuration
domain_name = "{{PROJECT_NAME}}.com"
create_route53_records = true
enable_dns_failover = true

# Monitoring Configuration
enable_cloudwatch_alarms = true
enable_detailed_monitoring = true
log_retention_days = 90

# Cost Optimization
enable_spot_instances = false
enable_reserved_instances = true

# Backup Configuration
backup_schedule = "0 2 * * *"  # Daily at 2 AM
backup_retention_days = 90
enable_point_in_time_recovery = true

# Auto Scaling Configuration
scale_up_threshold = 60
scale_down_threshold = 40
scale_up_adjustment = 2
scale_down_adjustment = -1
scale_up_cooldown = 300
scale_down_cooldown = 300

# Load Balancer Configuration
lb_idle_timeout = 300
lb_connection_draining_timeout = 600
lb_cross_zone_load_balancing = true
enable_access_logs = true

# Security Groups
allowed_cidr_blocks = [
  "10.2.0.0/16",     # Production VPC CIDR
]

# Enable/Disable Features
enable_nat_gateway = true
enable_vpn_gateway = true
enable_flow_logs   = true
enable_config      = true
enable_cloudtrail  = true

# Resource Tags
tags = {
  Environment        = "production"
  Project           = "{{PROJECT_NAME}}"
  Owner             = "{{GITHUB_USERNAME}}"
  CostCenter        = "production"
  Backup            = "critical"
  Monitoring        = "comprehensive"
  CreatedBy         = "terraform"
  ManagedBy         = "devops-team"
  Purpose           = "production-workload"
  DataClassification = "confidential"
  Compliance        = "soc2,pci-dss,gdpr"
}

# Production-specific settings
enable_debug_logging = false
enable_development_tools = false
skip_final_snapshot = false

# Container Configuration
container_cpu    = 2048
container_memory = 4096
container_port   = 8000

# ECS Configuration (if using ECS)
ecs_cluster_name = "{{PROJECT_NAME}}-production-cluster"
ecs_service_desired_count = 5
ecs_task_cpu = 2048
ecs_task_memory = 4096
ecs_enable_service_discovery = true

# Lambda Configuration (if using Lambda)
lambda_runtime = "nodejs18.x"
lambda_timeout = 300
lambda_memory_size = 1024
lambda_reserved_concurrency = 100

# API Gateway Configuration (if using API Gateway)
api_gateway_stage = "v1"
api_gateway_throttle_rate_limit = 10000
api_gateway_throttle_burst_limit = 20000
enable_api_caching = true

# CloudFront Configuration
cloudfront_price_class = "PriceClass_All"
cloudfront_enable_compression = true
cloudfront_default_ttl = 86400
cloudfront_max_ttl = 31536000
cloudfront_enable_ipv6 = true

# ElastiCache Configuration
elasticache_engine = "redis"
elasticache_node_type = "cache.r6g.xlarge"
elasticache_replication_group_size = 3
elasticache_port = 6379
elasticache_automatic_failover = true

# S3 Configuration
s3_versioning_enabled = true
s3_lifecycle_enabled = true
s3_transition_to_ia_days = 30
s3_transition_to_glacier_days = 90
s3_transition_to_deep_archive_days = 365
s3_expiration_days = 2555  # 7 years

# SNS Configuration
sns_email_endpoint = "alerts@{{PROJECT_NAME}}.com"
enable_sms_alerts = true
sms_endpoint = "+1234567890"

# SQS Configuration
sqs_visibility_timeout_seconds = 300
sqs_message_retention_seconds = 1209600
sqs_delay_seconds = 0
enable_dead_letter_queue = true

# Production Access (Restricted)
production_access_cidrs = [
  "203.0.113.0/24",  # Office network
  "198.51.100.0/24", # VPN network
]

# Database Production Settings
db_publicly_accessible = false
db_skip_final_snapshot = false
db_copy_tags_to_snapshot = true
db_auto_minor_version_upgrade = false
db_apply_immediately = false

# Performance Insights
db_performance_insights_enabled = true
db_performance_insights_retention_period = 31

# Enhanced Monitoring
db_monitoring_interval = 15
db_monitoring_role_arn = "arn:aws:iam::123456789012:role/rds-monitoring-role"

# Production Database Options
db_option_group_name = "{{PROJECT_NAME}}-production-options"
db_parameter_group_name = "{{PROJECT_NAME}}-production-params"

# Secret Manager Configuration
secrets_recovery_window_in_days = 30

# IAM Configuration
create_iam_roles = true
iam_path = "/{{PROJECT_NAME}}/production/"

# KMS Configuration
kms_deletion_window_in_days = 30
enable_kms_key_rotation = true

# WAF Configuration
enable_waf = true
waf_rate_limit = 10000
waf_block_malicious_ips = true
enable_ddos_protection = true

# CloudWatch Configuration
cloudwatch_log_group_retention_in_days = 90
enable_cloudwatch_logs = true
enable_x_ray_tracing = true

# Security Configuration
enable_guard_duty = true
enable_security_hub = true
enable_config_rules = true
enable_inspector = true
enable_macie = true

# Compliance Configuration
enable_compliance_monitoring = true
compliance_standards = ["SOC2", "PCI-DSS", "GDPR", "HIPAA"]

# Disaster Recovery
enable_cross_region_backups = true
enable_automated_failover = true
rto_minutes = 30  # Recovery Time Objective
rpo_minutes = 15  # Recovery Point Objective

# Notification Configuration
notification_endpoints = [
  "production-alerts@{{PROJECT_NAME}}.com",
  "devops@{{PROJECT_NAME}}.com",
  "security@{{PROJECT_NAME}}.com"
]

# SSL/TLS Configuration
certificate_transparency_logging = true
enable_hsts = true
hsts_max_age = 31536000

# Data Retention Policies
log_retention_policy = "90_days"
metric_retention_policy = "1_year"
backup_retention_policy = "90_days"
audit_log_retention_policy = "7_years"

# High Availability Configuration
enable_multi_az_deployment = true
enable_auto_failover = true
health_check_grace_period = 300

# Capacity Planning
expected_daily_requests = 10000000
peak_requests_per_second = 5000
data_growth_rate_per_month = "10%"

# Feature Flags for Production
feature_flags = {
  new_ui_enabled           = false  # Conservative approach
  beta_features_enabled    = false
  analytics_enabled        = true
  monitoring_enabled       = true
  caching_enabled         = true
  rate_limiting_enabled   = true
  authentication_required = true
}

# Security Hardening
enable_security_headers = true
enable_content_security_policy = true
enable_cors = true
cors_allowed_origins = [
  "https://{{PROJECT_NAME}}.com",
  "https://www.{{PROJECT_NAME}}.com"
]

# Third-party Integrations
enable_datadog_integration = true
enable_newrelic_integration = true
enable_sentry_integration = true
enable_pagerduty_integration = true

# Content Delivery Network
enable_cdn = true
cdn_regions = ["global"]
cdn_cache_behaviors = {
  "/api/*" = {
    ttl = 0
    compress = true
  }
  "/static/*" = {
    ttl = 86400
    compress = true
  }
}

# Database Configuration
enable_read_replicas = true
read_replica_count = 3
read_replica_instance_class = "db.r5.large"
enable_aurora_cluster = true
aurora_cluster_size = 3

# Search Configuration (if using Elasticsearch)
elasticsearch_version = "7.10"
elasticsearch_instance_type = "r6g.large.elasticsearch"
elasticsearch_instance_count = 3
elasticsearch_dedicated_master_enabled = true
elasticsearch_dedicated_master_count = 3

# Queue Configuration
enable_message_queuing = true
queue_visibility_timeout = 300
dead_letter_queue_enabled = true
enable_fifo_queues = true

# File Storage Configuration
enable_efs = true
efs_performance_mode = "generalPurpose"
efs_throughput_mode = "provisioned"
efs_provisioned_throughput = 100

# Container Registry
enable_ecr = true
ecr_image_scanning = true
ecr_lifecycle_policy = true

# Secrets Management
enable_secrets_manager = true
enable_parameter_store = true
secrets_rotation_enabled = true

# Audit Configuration
enable_audit_logging = true
audit_log_destinations = [
  "cloudwatch",
  "s3",
  "elasticsearch"
]

# Cost Management
enable_cost_anomaly_detection = true
cost_budget_amount = 10000
cost_budget_time_unit = "MONTHLY"

# Performance Configuration
enable_performance_insights = true
enable_enhanced_monitoring = true
enable_slow_query_logging = true

# Network Security
enable_vpc_endpoints = true
enable_private_dns = true
enable_network_acls = true

# Database Security
enable_db_encryption = true
db_kms_key_id = "alias/{{PROJECT_NAME}}-production-db"
enable_db_activity_stream = true

# Application Security
enable_application_firewall = true
enable_ip_whitelisting = true
enable_geo_blocking = true
blocked_countries = ["XX", "YY"]  # Replace with actual country codes

# Maintenance Windows
maintenance_windows = {
  database = "sun:04:00-sun:06:00"
  cache    = "sun:06:00-sun:07:00"
  compute  = "sun:02:00-sun:04:00"
}

# Production Specific Variables
production_mode = true
debug_enabled = false
verbose_logging = false
mock_external_services = false
disable_authentication = false
