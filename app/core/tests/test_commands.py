"""
Test custom Django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db(self, patched_check):
        """Testing the wait for db command"""
        # Mock the database is up
        patched_check.return_value = True

        call_command('wait_for_db')

        # Assert that we are calling with the correct value
        patched_check.assert_called_once_with(databases=['default'])

    # Patch sleep so that any sleep calls run without sleeping
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        # This patch returns 2 Psycopg2Errors, 3 OperationalErrors 
        # and then finally True. aka emulating slow starting db
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        # Make sure it only calls 6 times as we have 6 patch returns
        self.assertEqual(patched_check.call_count, 6)

        # Assert that we are calling with the correct value
        patched_check.assert_called_with(databases=['default'])
    