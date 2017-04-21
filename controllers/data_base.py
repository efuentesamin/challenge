import os

import sqlite3

from clients.ebay import EBayClient


class DataBaseController:
    _db_name = 'categories.db'
    _connection = None

    def rebuild(self):
        """
        Deletes and rebuild the db filling records from eBay API
        :return: 
        """
        # Delete current db
        print('--------> Deleting current db...')

        try:
            os.remove(self._db_name)
        except FileNotFoundError:
            pass

        # Create fresh new db
        self._create_db()
        # Get categories from eBay
        categories = EBayClient.get_categories()

        # Bulk insert categories in db
        for category in categories:
            self.insert_category(category)

        print('--------> {} records inserted!'.format(len(categories)))

    def _create_db(self):
        """
        Create daba base tables
        :return: 
        """
        print('--------> Creating new db...')
        conn = self._get_connection()
        cursor = conn.cursor()

        # Create table
        cursor.execute("""
            CREATE TABLE categories (
              id int, 
              name text, 
              level int, 
              parent int, 
              best_offer boolean, 
              expired boolean, 
              leaf boolean
            )
        """)
        # Commit the changes
        conn.commit()
        print('--------> New db created!')

    def _get_connection(self):
        """
        Initialize the data base connection
        :return: Data base connection
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_name)

        return self._connection

    def insert_category(self, category):
        """
        Inserts the collection categories in db
        :param categories: List of categories objects
        :return: 
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        # Insert record
        cursor.execute(
            """INSERT INTO categories VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                category.id,
                category.name,
                category.level,
                category.parent,
                category.best_offer,
                category.expired,
                category.leaf
            )
        )
        # Commit the changes
        conn.commit()
