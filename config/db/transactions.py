import psycopg


class Transaction:
    def __init__(self, connection: psycopg.Connection):
        """
        Receive an active database connection via psycopg.connect().
        """
        self.conn = connection

    def create_blood_centers(self):
        query = """
        CREATE TABLE IF NOT EXISTS blood_centers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute_query(query)

    def create_blood_types(self):
        query = """
        CREATE TABLE IF NOT EXISTS blood_types (
            id SERIAL PRIMARY KEY,
            name VARCHAR UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._execute_query(query)

    def create_blood_center_stocks(self):
        query = """
        CREATE TABLE IF NOT EXISTS blood_center_stocks (
            id SERIAL PRIMARY KEY,
            blood_center_id INTEGER NOT NULL,
            collected_at DATE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_blood_center
                FOREIGN KEY (blood_center_id)
                REFERENCES blood_centers (id)
        );
        """
        self._execute_query(query)

    def create_blood_stock_items(self):
        query = """
        CREATE TABLE IF NOT EXISTS blood_stock_items (
            id SERIAL PRIMARY KEY,
            blood_center_stock_id INTEGER NOT NULL,
            blood_type_id INTEGER NOT NULL,
            status VARCHAR NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_blood_center_stock
                FOREIGN KEY (blood_center_stock_id)
                REFERENCES blood_center_stocks (id),
            CONSTRAINT fk_blood_type
                FOREIGN KEY (blood_type_id)
                REFERENCES blood_types (id),
            CONSTRAINT unique_stock_type
                UNIQUE (blood_center_stock_id, blood_type_id)
        );
        """
        self._execute_query(query)

    def create_all(self):
        """
        Executes the creation of all tables in the exact order of dependency
        of Foreign Keys.
        """
        try:
            self.create_blood_centers()
            self.create_blood_types()
            self.create_blood_center_stocks()
            self.create_blood_stock_items()
            self.conn.commit()
            print("Create Tables sucessfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating tables: {e}")

    def drop_all(self):
        """
        Executes the drop of all tables and your dependencies.
        """
        query = """
            DROP TABLE IF EXISTS blood_stock_items,
                                blood_center_stocks,
                                blood_types,
                                blood_centers CASCADE;
        """
        try:
            self._execute_query(query)
            self.conn.commit()
            print("Drop Tables successfully.")
        except Exception as e:
            self.conn.rollback()
            print(f"Error dropping tables: {e}")


    def insert_blood_type(self, name: str):
        query = """
            INSERT INTO blood_types (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """
        self._execute_query(query, (name,))

    def _execute_query(self, query: str, params: tuple | None = None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
