import psycopg2
import pandas as pd

from sqlalchemy import create_engine

class Postgresql():
    """
    A class that handles the Postgresql connections and execution of commands
    """
    
    def __init__(self, config):
        self.database = config['database']
        self.user = config['user']
        self.password = config['pass']
        self.host = config['host']
        self.port = config['port']
    
    def conn_string(self):
        """
        Generates the connection string
        """
        
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            
    def execute_command(self, command, query = False):
        """
        Executes either commands (DDL) or queries (DML) and returns the result from the query
        """
        
        try:
            conn = psycopg2.connect(self.conn_string())
            cursor = conn.cursor()
            cursor.execute(command)
            if query:
                result = pd.DataFrame(cursor.fetchall())
            else:
                result = "Command executed."
            conn.commit()
            conn.close()
            
            return result
        except Exception as e:
            print(f"Error while executing command: {str(e)}")
            
    def query_table(self, query):
        """
        Executes a query statement
        """
        
        return self.execute_command(query, query = True)
            
    def upload_table(self, df, table_name):
        """
        Uploads a dataframe to a given table
        """
        
        try:
            db = create_engine(self.conn_string())
            conn = db.connect()
            df.to_sql(table_name, con=conn, if_exists='replace', index=False) # Using replace (can use append too)
            conn = psycopg2.connect(self.conn_string())
            cursor = conn.cursor()
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error while uploading table: {str(e)}")
