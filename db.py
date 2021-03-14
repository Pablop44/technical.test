from neo4j import GraphDatabase, basic_auth
from configparser import ConfigParser


class Database:
    def __init__(self):
        parser = ConfigParser()
        parser.read('./config/config.dat')
        SOCKET_TO_CONNECT = parser.get('common_configuration', 'socket_to_connect')
        USER = parser.get('common_configuration', 'user')
        PASSWORD = parser.get('common_configuration', 'password')
        DATABASE = parser.get('common_configuration', 'database')
        self.driver = GraphDatabase.driver(
            SOCKET_TO_CONNECT,
            auth=basic_auth(USER, PASSWORD)).session(database=DATABASE)

    def execute_query_read(self, cypher_query):
        with self.driver as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
            self.driver.close()
            return results

    def execute_query_write(self, cypher_query):
        with self.driver as session:
            results = session.write_transaction(
                lambda tx: tx.run(cypher_query).data())
            self.driver.close()
            return results

    def close_database_connection(self):
        self.driver.close()
