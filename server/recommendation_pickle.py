from sklearn.externals import joblib
import  pandas as pd


class recommendationPickle:

    def get_recommendation_from_pickle(menu_api, list_of_ingredients):
        testData = []

        for each in list_of_ingredients:
            ingredients_string = each.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            ingredients_string = ingredients_string.replace('"', ' ')
            ingredients_string = ingredients_string.translate({ord(c): " " for c in '0123456789'})
            testData.append(ingredients_string)


        testDataFrame = pd.DataFrame(testData, columns=['ingredients'])
        testDataFrame = testDataFrame.replace('-', ' ', regex=True)
        x_test = testDataFrame.iloc[:, 0].values
        vect = joblib.load('pickles/vector_pickle.pkl')
        x_test_vectorized = vect.transform(x_test)

        clf = joblib.load('pickles/prediction_pickle.pkl')
        result = clf.predict(x_test_vectorized)
        index_list = [index for index, value in enumerate(result) if value == 1]
        result_api = []
        for each in index_list:
            result_api.append(menu_api[each])

        return result_api