import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score


class LearningModule:

    def predictResult():

        foodToAvoid = ['white rice', 'pasta', 'white bread', 'bagels', 'white flour tortillas',
                       'crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb',
                       'fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep-fried', 'whole milk', 'full-fat',
                       'sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream',
                       'fries', 'doughnuts',
                       'croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons',
                       'pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster',
                       'honey'
                       'potsticker', 'potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour']

        dataset = pd.read_json("data/train.json")
        ingr = dataset["ingredients"]
        listOfIngredients = []
        classificationList = [1] * 39774

        count = 0

        for i in ingr:
            for j in foodToAvoid:
                if j in i:
                    classificationList[count] = 0
            count = count + 1

        for i in ingr:
            data = ' '.join(i)
            print(data)
            listOfIngredients.append(data)

        ingradients = pd.DataFrame(listOfIngredients, columns=['ingradients'])
        ingradients = ingradients.replace('-', ' ', regex=True)
        values = pd.DataFrame(classificationList, columns=['value'])
        mainDataFrame = ingradients.join(values)
        # print(mainDataFrame)
        # mainDataFrame.to_csv("Data.csv", index=True)
        x = mainDataFrame.iloc[:, 0].values
        # print(x)
        y = mainDataFrame.iloc[:, 1].values
        # print(y)

        '''
        testDataList = []

        for i in range(0, len(testList)):
            res = " ".join(testList[i])
            testDataList.append(res)

        # print(testDataList)
        
        testDataFrame = pd.DataFrame(testDataList, columns=['ingredients'])
        testDataFrame = testDataFrame.replace('-', ' ', regex=True)
        # print(testDataFrame)
        xTest = testDataFrame.iloc[:, 0].values
        # print(xTest)
        '''





        vectorizer = TfidfVectorizer()
        x_vct = vectorizer.fit_transform(x)
        x_train, x_test, y_train, y_test = train_test_split(x_vct, y, test_size=0.3, random_state=0)
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier(random_state=0)
        clf.fit(x_train, y_train)
        predResults = clf.predict(x_test)
        print(predResults)
        print("Accuracy : "+str(accuracy_score(y_test, predResults)))
        '''
        xTest_vct = vectorizer.transform(xTest)
        # print(xTest_vct)
        testRes = clf.predict(xTest_vct)
        # print(testRes)
        return testRes
        '''

'''
testList = [["olive oil","purple onion","fresh pineapple","pork","poblano peppers","corn tortillas","cheddar cheese",
                        "ground black pepper","salt","iceberg lettuce","lime","jalapeno chilies",
                        "chopped cilantro fresh"],
            ["roma tomatoes","kosher salt","purple onion","jalapeno chilies","lime",
                        "chopped cilantro"]]




'''






