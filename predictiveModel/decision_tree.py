from sklearn.tree import DecisionTreeClassifier

from models.DataSet import DataSet


class Decision_tree:
    def __init__(self):
        self.dataSet = DataSet()
        self.classifier = DecisionTreeClassifier(random_state=0)
        self.clf = None

    def fit(self, id):
        data_without_user = self.dataSet.get_dataset_without_information_user(id)
        data_of_user_to_predict = self.dataSet.get_dataset_information_user(id)
        y_fit = data_without_user[["name"]]
        X_fit = data_without_user.loc[:, data_without_user.columns != 'name']
        self.clf = self.classifier.fit(X_fit, y_fit)
        data_frame_to_predict = data_of_user_to_predict.loc[:, data_of_user_to_predict.columns != 'name']
        return self.predict(data_frame_to_predict)

    def predict(self, data_frame):
        return self.clf.predict(data_frame)
