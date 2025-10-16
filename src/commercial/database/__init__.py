"""
PostgreSQL Database Schema for Commercial SaaS Infrastructure

This module defines the database models and schema for the multi-tenant
commercial platform, replacing placeholder methods with persistent storage.

Author: ChrisClements1987
"""

import os
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from enum import Enum

# Database imports
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import SimpleConnectionPool

    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    # Create mock classes for testing when psycopg2 is not available
    class SimpleConnectionPool:
        """Mock SimpleConnectionPool for testing when psycopg2 is not available."""

        def __init__(self, minconn, maxconn, dsn):
            pass

        def getconn(self):
            return None

        def putconn(self, conn):
            pass

        def closeall(self):
            pass

    class RealDictCursor:
        """Mock RealDictCursor for testing when psycopg2 is not available."""

        pass

    logging.warning("PostgreSQL not available. Install psycopg2 for database support.")

from ..models import (
    Customer,
    Organization,
    Subscription,
    UsageMetrics,
    CustomerStatus,
    SubscriptionPlan,
    OrganizationStatus,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages PostgreSQL database connections and operations for commercial infrastructure.
    """

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.

        Args:
            database_url: PostgreSQL connection string
        """
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.pool = None
        self._initialize_connection()

    def _initialize_connection(self):
        """Initialize database connection pool."""
        if not DATABASE_AVAILABLE:
            logger.warning("Database not available - using in-memory storage")
            return

        if not self.database_url:
            logger.warning("No DATABASE_URL provided - using in-memory storage")
            return

        try:
            self.pool = SimpleConnectionPool(
                minconn=1, maxconn=10, dsn=self.database_url
            )
            self._create_tables()
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            self.pool = None

    def _create_tables(self):
        """Create database tables if they don't exist."""
        if not self.pool:
            return

        create_tables_sql = """
        -- Customers table
        CREATE TABLE IF NOT EXISTS customers (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            company_name VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'active',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            settings JSONB DEFAULT '{}'::jsonb
        );

        -- Organizations table
        CREATE TABLE IF NOT EXISTS organizations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'active',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            config JSONB DEFAULT '{}'::jsonb
        );

        -- Subscriptions table
        CREATE TABLE IF NOT EXISTS subscriptions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
            plan VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'active',
            start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            end_date TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );

        -- Usage metrics table
        CREATE TABLE IF NOT EXISTS usage_metrics (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
            organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
            metric_name VARCHAR(100) NOT NULL,
            metric_value DECIMAL(15,2) NOT NULL,
            recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            metadata JSONB DEFAULT '{}'::jsonb
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
        CREATE INDEX IF NOT EXISTS idx_organizations_customer_id ON organizations(customer_id);
        CREATE INDEX IF NOT EXISTS idx_subscriptions_customer_id ON subscriptions(customer_id);
        CREATE INDEX IF NOT EXISTS idx_usage_metrics_customer_id ON usage_metrics(customer_id);
        CREATE INDEX IF NOT EXISTS idx_usage_metrics_recorded_at ON usage_metrics(recorded_at);
        """

        try:
            with self.pool.getconn() as conn:
                with conn.cursor() as cur:
                    cur.execute(create_tables_sql)
                    conn.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def get_connection(self):
        """Get a database connection from the pool."""
        if not self.pool:
            return None
        return self.pool.getconn()

    def return_connection(self, conn):
        """Return a connection to the pool."""
        if self.pool and conn:
            self.pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """
        Execute a database query.

        Args:
            query: SQL query string
            params: Query parameters
            fetch: Whether to fetch results

        Returns:
            Query results if fetch=True, otherwise None
        """
        if not self.pool:
            # Fallback to in-memory storage for testing
            return self._execute_in_memory(query, params, fetch)

        try:
            with self.pool.getconn() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetch:
                        return cur.fetchall()
                    conn.commit()
                    return cur.rowcount
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            raise

    def _execute_in_memory(self, query: str, params: tuple = None, fetch: bool = False):
        """Execute query using in-memory storage for testing."""
        # Simple in-memory storage for testing
        if not hasattr(self, "_in_memory_data"):
            self._in_memory_data = {
                "customers": [],
                "organizations": [],
                "subscriptions": [],
                "usage_metrics": [],
            }

        # Parse query type
        query_lower = query.lower().strip()

        if query_lower.startswith("insert into customers"):
            # Create customer
            customer_id = f"cust_{len(self._in_memory_data['customers']) + 1}"
            customer = {
                "id": customer_id,
                "email": params[0],
                "company_name": params[1],
                "status": params[2],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "settings": params[3] if len(params) > 3 else {},
            }
            self._in_memory_data["customers"].append(customer)
            return [customer] if fetch else 1

        elif query_lower.startswith("select") and "customers" in query_lower:
            # Query customers
            if params and len(params) == 1:  # email or id lookup
                lookup_value = params[0]
                for customer in self._in_memory_data["customers"]:
                    if (
                        customer["email"] == lookup_value
                        or customer["id"] == lookup_value
                    ):
                        return [customer] if fetch else 1
                return [] if fetch else 0
            return (
                self._in_memory_data["customers"]
                if fetch
                else len(self._in_memory_data["customers"])
            )

        elif query_lower.startswith("insert into subscriptions"):
            # Create subscription
            subscription = {
                "id": f"sub_{len(self._in_memory_data['subscriptions']) + 1}",
                "customer_id": params[0],
                "plan": params[1],
                "status": params[2],
                "start_date": params[3],
                "end_date": params[4] if len(params) > 4 else None,
            }
            self._in_memory_data["subscriptions"].append(subscription)
            return [subscription] if fetch else 1

        elif query_lower.startswith("select") and "subscriptions" in query_lower:
            # Query subscriptions
            if params and len(params) == 1:  # customer_id lookup
                customer_id = params[0]
                matching_subs = []
                for sub in self._in_memory_data["subscriptions"]:
                    if sub["customer_id"] == customer_id:
                        matching_subs.append(sub)
                return matching_subs if fetch else len(matching_subs)
            return (
                self._in_memory_data["subscriptions"]
                if fetch
                else len(self._in_memory_data["subscriptions"])
            )

        return [] if fetch else 0

    def close(self):
        """Close the database connection pool."""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection pool closed")


# Global database manager instance
db_manager = DatabaseManager()


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    return db_manager
