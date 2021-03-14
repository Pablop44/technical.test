from models.DataSet import DataSet
import pandas as pd


def create_dataset_recomendations(data_of_similar_user, data_of_initial_user, books):
    books_red = data_of_initial_user['title'].tolist()
    books.drop(books[books['title'].isin(books_red)].index, inplace=True)
    result = pd.merge(data_of_similar_user, books, how="outer", on=["title", "genre"])
    books_red = data_of_initial_user['title'].tolist()
    result.drop(result[result['title'].isin(books_red)].index, inplace=True)
    return result.fillna(2.5)


class Reviser:
    def __init__(self):
        self.dataSet = DataSet()

    def get_recommendations(self, similar_user, id_initial_user):
        data_of_similar_user = self.dataSet.get_punctuations_by_username(similar_user)
        data_of_initial_user, name = self.dataSet.get_punctuations_by_id(id_initial_user)
        books = self.dataSet.get_books(True)

        df_recommendations = create_dataset_recomendations(data_of_similar_user, data_of_initial_user, books)

        return df_recommendations, name

