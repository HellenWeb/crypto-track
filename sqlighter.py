# Modules

import sqlite3 as sql

# Sqlighter - Class


class Sqlighter:
    def __init__(self, db):
        self.connect = sql.connect(db)
        self.cursor = self.connect.cursor()

    def show_info(self, user_id):
        with self.connect:
            return self.cursor.execute(
                "SELECT * FROM `persons` WHERE `user_id` = ?", (user_id,)
            ).fetchall()

    def inster_name(self, user_id, name):
        with self.connect:
            self.cursor.execute(
                f'INSERT INTO `users` (`user_id`, `name`) VALUES ("{user_id}", "{name}")'
            )

    def update_name(self, user_id, name):
        with self.connect:
            self.cursor.execute(
                f'UPDATE `users` SET `name` = "{name}" WHERE `user_id` = {user_id}'
            )

    def inster_currency(self, user_id, currency):
        with self.connect:
            self.cursor.execute(
                f'INSERT INTO `users` (`user_id`, `currency`) VALUES ("{user_id}", "{currency}")'
            )

    def update_currency(self, user_id, currency):
        with self.connect:
            self.cursor.execute(
                f"UPDATE `users` SET `currency` = {currency} WHERE `user_id` = {user_id}"
            )
