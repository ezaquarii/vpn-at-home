"""
This app contains app management functionality and related utilities.

 * Settings model contains application-wide, dynamic settings, such as registration enablement and SMTP configuration.
 * CRUD API for superuser
 * generic mail utilities
"""


def is_database_migrated(database='default'):
    from django.db import connections
    from django.db.migrations.loader import MigrationLoader
    if database in connections:
        loader = MigrationLoader(connections[database])
        all_migrations = loader.graph.nodes.keys()
        applied = loader.applied_migrations
        return all([migration in applied for migration in all_migrations])
    else:
        return False
