import sqlite3
from climbing_route import ClimbingRoute


class ClimbingRouteDao:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS climbing_routes")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS climbing_routes ("
            "route_id INTEGER PRIMARY KEY,"
            "user_id INTEGER,"
            "name TEXT,"
            "grade TEXT,"
            "FOREIGN KEY(user_id) REFERENCES users(id)"
            ")"
        )
        self.conn.commit()

    def add_route(self, route, user_id):
        if user_id != 1:
            raise PermissionError("Only the admin can add routes.")
        self.cursor.execute(
            "INSERT INTO climbing_routes (user_id, name, grade) VALUES (?, ?, ?)",
            (route.user_id, route.name, route.grade),
        )
        self.conn.commit()

    def get_route(self, route_id):
        self.cursor.execute(
            "SELECT * FROM climbing_routes WHERE route_id = ?",
            (route_id,)
        )
        row = self.cursor.fetchone()
        if row:
            return ClimbingRoute(row[0], row[1], row[2], row[3])
        return None

    def get_all_routes(self):
        self.cursor.execute("SELECT * FROM climbing_routes")
        rows = self.cursor.fetchall()
        return [ClimbingRoute(row[0], row[1], row[2], row[3]) for row in rows]

    def update_route(self, route, user_id):
        if user_id != 1:
            raise PermissionError("Only the admin can update routes.")
        self.cursor.execute(
            "UPDATE climbing_routes SET name = ?, grade = ? WHERE route_id = ?",
            (route.name, route.grade, route.route_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_route(self, route_id, user_id):
        if user_id != 1:
            raise PermissionError("Only the admin can delete routes.")
        self.cursor.execute(
            "DELETE FROM climbing_routes WHERE route_id = ?",
            (route_id,),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
