import os

import sqlite3

from clients.ebay import EBayClient
from models import Category


class DataBaseController:
    _db_name = 'categories.db'

    def __init__(self):
        self._connection = sqlite3.connect(self._db_name)

    def rebuild(self):
        """
        Deletes and rebuild the db filling records from eBay API
        :return: 
        """
        # Delete current db
        print('--------> Deleting current db...')

        try:
            self._connection.close()
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
        self._connection = sqlite3.connect(self._db_name)
        cursor = self._connection.cursor()

        # Create table
        cursor.execute("""CREATE TABLE categories (id int, name text, level int, parent int, best_offer boolean, expired boolean, leaf boolean)""")
        # Commit the changes
        self._connection.commit()
        print('--------> New db created!')

    def insert_category(self, category):
        """
        Inserts the collection categories in db
        :param category: List of categories objects
        :return: 
        """
        cursor = self._connection.cursor()
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
        self._connection.commit()

    def get_category_by_id(self, category_id):
        """
        Finds a category by id in db.
        :param category_id: Category id
        :return: 
        """
        cursor = self._connection.cursor()
        # Query db
        cursor.execute("""SELECT * FROM categories WHERE id = ?""", (category_id, ))
        row = cursor.fetchone()
        category = Category(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        print(category)
        self._get_children(category)
        return category

    def _get_children(self, category):
        cursor = self._connection.cursor()
        # Query db
        cursor.execute("""SELECT * FROM categories WHERE parent = ? AND id != ?""", (category.id, category.id))
        rows = cursor.fetchall()

        for row in rows:
            child = Category(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            print(child)
            self._get_children(child)
            category.children.append(child)
