import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

'''
reading json data and creating pandas series which will be letter used to 
create pandas dataframe of ingredients and their classification
'''
train_dataset = pd.read_json("data/train.json");
ingredients_data = train_dataset["ingredients"];
#print(type(ingredients_data))


'''
list_of_ingredients will have ingredients for receipe and 
classification_list will have value 0 - bad or 1 - good 
'''
list_of_ingredients = []
classification_list = []
food_to_avoid = ['white rice', 'pasta', 'white bread', 'bagels', 'white flour tortillas','crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb','fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep fried', 'whole milk', 'full fat','sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream', 'fries','doughnuts','croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons','pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster', 'honey''potsticker','potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour']



for each in ingredients_data:
    receipe_ingredients = ' '.join(each)
    receipe_ingredients.replace('-',' ')
    list_of_ingredients.append(receipe_ingredients)


for each in list_of_ingredients:
    count = 0
    value = 1
    for each_item in food_to_avoid:
        if each_item in each:
            value = 0
    classification_list.append(value)


'''
creating a pandas dataframe from list_of_ingredients and their clasification value
pandas dataframe will be used in creating a train and test data for machine learning module
'''
ingredients_dataframe =  pd.DataFrame(list_of_ingredients,columns=['ingredients'])
ingredients_dataframe = ingredients_dataframe.replace('-',' ',regex=True)
classification_dataframe = pd.DataFrame(classification_list, columns=['classification_value'])
main_dataframe = ingredients_dataframe.join(classification_dataframe)


x_ingredients = main_dataframe.iloc[:,0].values
y_classification_values = main_dataframe.iloc[:,1].values

vectorizor = TfidfVectorizer()
x_ingredients_vectorized = vectorizor.fit_transform(x_ingredients)
x_train, x_test, y_train, y_test = train_test_split(x_ingredients_vectorized,y_classification_values, test_size=0.3, random_state=0)
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x_train,y_train)

results = clf.predict(x_test)
print("\n Accuracy: ")
print(str(accuracy_score(y_test,results)))

