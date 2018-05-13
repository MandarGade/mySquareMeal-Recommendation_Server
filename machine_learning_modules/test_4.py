import pandas as pd
import json
import re

file = open('../data/eatstreet_data.json','r')
eatstreet_data = json.load(file)

NAME_DESCRIPTION_LIST=[]
NUMERIC_STRING_LIST=[]
FOOD_TO_AVOID = ['jasmin rice','white rice', 'pasta', 'white bread', 'bagels', 'white flour','white flour tortillas','crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb','fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep fried', 'whole milk', 'full fat','sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream', 'fries','doughnuts','croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons','pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster', 'honey''potsticker','potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour']
FOOD_TO_AVOID_NUMERIC = []
#CLASSIFICATION_LIST = [1] * (len(NAME_DESCRIPTION_LIST)+1)
CLASSIFICATION_LIST=[]
for each in eatstreet_data:
	dict_data = each["menu"]
	for each in dict_data:
		items_data=each["items"]
		for each in items_data:
			item_name=each["name"]
			name=re.sub('[^A-Za-z\s]+', '', item_name)
			if "description" in each:
				item_description=each["description"]
				description = re.sub('[^A-Za-z\s]+', '', item_description)
				NAME_DESCRIPTION_LIST.append((name+description).lower())
			else:
				NAME_DESCRIPTION_LIST.append((name).lower())


NAME_DESCRIPTION_LIST += FOOD_TO_AVOID


for food_name in NAME_DESCRIPTION_LIST:
	value = None
	if any(word in food_name for word in FOOD_TO_AVOID):
		value=0
		
	else:
		value=1

	CLASSIFICATION_LIST.append(value)


'''

for each_string in NAME_DESCRIPTION_LIST:
	numeric_string=''
	for i in range(0,len(each_string)):
		numeric_string += str(ord(each_string[i]))

	NUMERIC_STRING_LIST.append(numeric_string)

for each_string in FOOD_TO_AVOID:
	numeric_string=''
	for i in range(0,len(each_string)):
		numeric_string +=str(ord(each_string[i]))
	FOOD_TO_AVOID_NUMERIC.append(numeric_string)



count = 0
for each_numeric_string in NUMERIC_STRING_LIST:
	value = None
	if any(avoid_numeric_string in each_numeric_string for avoid_numeric_string in FOOD_TO_AVOID_NUMERIC):
		value = 0
		count +=1
	else:
		value = 1

	CLASSIFICATION_LIST.append(value)


#print(len(NUMERIC_STRING_LIST))
#print(len(CLASSIFICATION_LIST))
'''

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle
from sklearn import tree
from sklearn.feature_extraction.text import TfidfVectorizer




ingredients_dataframe =  pd.DataFrame(NAME_DESCRIPTION_LIST,columns=['ingredients'])
classification_dataframe = pd.DataFrame(CLASSIFICATION_LIST, columns=['classification_value'])
main_dataframe = ingredients_dataframe.join(classification_dataframe)


x_ingredients = main_dataframe.iloc[:,0].values
#print(x_ingredients)
y_classification = main_dataframe.iloc[:,1].values

vectorizor = TfidfVectorizer()
x_ingredients_vectorized = vectorizor.fit_transform(x_ingredients)


#print(x_ingredients)
#print(y_classification)

x_train, x_test, y_train, y_test = train_test_split(x_ingredients_vectorized,y_classification, test_size=0.3, random_state=0)
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x_train,y_train)
#results = clf.predict(x_test)
#print("\n Accuracy: ")
#print(str(accuracy_score(y_test,results)))


test_ingradients_vectorized=vectorizor.transform(['jasmin rice','white rice', 'pasta', 'white bread', 'bagels', 'white flour','white flour tortillas','crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb','fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep fried', 'whole milk', 'full fat','sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream', 'fries','doughnuts','croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons','pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster', 'honey''potsticker','potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour'])
res = clf.predict(test_ingradients_vectorized)
print(res)
print(list(res).count(0))
print(len(list(res)))
