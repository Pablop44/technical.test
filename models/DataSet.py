import db
import pandas as pd
from configparser import ConfigParser

EXPERT_MINIMUM_PUNCTUATION = 2.5


class DataSet:
    def __init__(self):
        self.connection = db.Database()

    def get_dataset_without_information_user(self, id):
        cypher_query = '''
         MATCH p=(u)-[r:rates]->(m) 
         WHERE u.id <> {} 
         RETURN u.name AS name, r.score as punctuation, m.title as title, m.genre as genre
        '''.format(str(id))

        result = self.connection.execute_query_read(cypher_query)
        df = pd.DataFrame([dict(row) for row in result])
        df = self.get_df_pivoted_and_full(df, index="name", columns="title", values="punctuation", fill_value=5)
        return df

    def get_dataset_information_user(self, id):
        query_punctuations_user = '''
        MATCH p=(u)-[r:rates]->(m) 
        WHERE u.id = {} 
        RETURN u.name AS name, r.score as punctuation, m.title as title, m.genre as genre
        '''.format(str(id))

        result = self.connection.execute_query_read(query_punctuations_user)
        df = pd.DataFrame([dict(row) for row in result])
        df = self.get_df_pivoted_and_full(df, index="name", columns="title", values="punctuation", fill_value=5)
        return df

    def get_books(self, genre):
        query_books = '''
        MATCH (m:book) 
        RETURN DISTINCT m.title as title
        '''

        if genre:
            query_books = '''
            MATCH (m:book) 
            RETURN DISTINCT m.title as title, m.genre as genre
            '''

        result = self.connection.execute_query_read(query_books)
        df = pd.DataFrame([dict(row) for row in result])
        return df

    def get_users(self):
        query_books = '''
        MATCH (m:User) 
        RETURN DISTINCT m.name as name, m.id as id
        '''

        result = self.connection.execute_query_read(query_books)
        df = pd.DataFrame([dict(row) for row in result])
        return df

    def insert_punctuation(self, name, score, book):
        query_book_punctuation = '''
        MATCH (u:User), (m:book)
        WHERE u.name = '%s' AND m.title = '%s' 
        MERGE (u)-[:rates{score:%d}]->(m)
        ''' % (name, book, score)

        result = self.connection.execute_query_write(query_book_punctuation)
        return result

    def get_punctuations_by_username(self, username):
        query_punctuation_by_username = '''
        MATCH (u:User)-[r:rates]-(m:book)
        WHERE u.name = '%s' AND r.score>%f
        RETURN m.title as title, m.genre as genre, r.score as score
        ''' % (username, EXPERT_MINIMUM_PUNCTUATION)

        result = self.connection.execute_query_write(query_punctuation_by_username)
        df = pd.DataFrame([dict(row) for row in result])
        return df

    def get_punctuations_by_id(self, id):
        query_punctuation_by_username = '''
        MATCH (u:User)-[r:rates]-(m:book)
        WHERE u.id = %d
        RETURN m.title as title, m.genre as genre, r.score as score
        ''' % (id)

        getName = '''
        MATCH (u:User)
        WHERE u.id = %d
        RETURN u.name as name
        ''' % (id)

        result = self.connection.execute_query_write(query_punctuation_by_username)
        result2 = self.connection.execute_query_write(getName)
        df = pd.DataFrame([dict(row) for row in result])
        return df, result2

    def get_df_pivoted_and_full(self, df, index, columns, values, fill_value):
        data_to_concat = self.get_books(False)
        finalDf = pd.concat([df, data_to_concat]).drop_duplicates()
        df_pivoted = finalDf.pivot(index=index, columns=columns, values=values).fillna(fill_value)
        df_pivoted.reset_index(inplace=True)
        return df_pivoted.rename_axis(None, axis=1).loc[1:, ]
