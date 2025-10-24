#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortuno.settings')
django.setup()

# Drop all tables
with connection.cursor() as cursor:
    cursor.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    """)

print("Database reset complete!")