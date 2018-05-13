import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pickle
from sklearn.externals import joblib
import pydotplus
from sklearn import tree
import collections

import time
start = time.time()

file = (open('../data/eatstreet_data.json','r'))
eatstreet_data = json.load(file)
#print(len(eatstreet_data))

food_to_avoid = ['white rice', 'pasta', 'white bread', 'bagels', 'white flour tortillas','crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb','fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep fried', 'whole milk', 'full fat','sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream', 'fries','doughnuts','croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons','pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster', 'honey''potsticker','potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour']

list_of_ingredients =[]
ingredients_data = []
classification_list = []

for each_record in eatstreet_data:
    menu = each_record["menu"]
    for menu_record in menu:
        menu_items = menu_record["items"]
        for each_menu_item in menu_items:
            if "description" in each_menu_item:
                #print(each_menu_item["name"]+" - "+each_menu_item["description"])
                ingredients_data.append(each_menu_item["name"]+" - "+each_menu_item["description"])
            else:
                #print((each_menu_item["name"]))
                ingredients_data.append(each_menu_item["name"])

for each in ingredients_data:
    ingredients_string = each.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
    ingredients_string = ingredients_string.replace('"',' ' )
    ingredients_string = ingredients_string.translate({ord(c): " " for c in '0123456789'})
    list_of_ingredients.append(ingredients_string)

#print(len(list_of_ingredients))

for each in list_of_ingredients:
    count = 0
    value = 1
    for each_item in food_to_avoid:
        if each_item in each:
            value = 0
    classification_list.append(value)

#print(len(classification_list))

ingredients_dataframe =  pd.DataFrame(list_of_ingredients,columns=['ingredients'])
ingredients_dataframe = ingredients_dataframe.replace('-',' ',regex=True)
classification_dataframe = pd.DataFrame(classification_list, columns=['classification_value'])
main_dataframe = ingredients_dataframe.join(classification_dataframe)


x_ingredients = main_dataframe.iloc[:,0].values
y_classification_values = main_dataframe.iloc[:,1].values

vectorizor = TfidfVectorizer()
x_ingredients_vectorized = vectorizor.fit_transform(x_ingredients)
joblib.dump(vectorizor,'vect_pickle.pkl')
x_train, x_test, y_train, y_test = train_test_split(x_ingredients_vectorized,y_classification_values, test_size=0.3, random_state=0)
'''
clf = DecisionTreeClassifier(random_state=0)

clf.fit(x_train,y_train)


joblib.dump(clf,'testPickle.pkl')
'''
clf = joblib.load('../pickles/testPickle.pkl')


results = clf.predict(x_test)
print("\n Accuracy: ")
print(str(accuracy_score(y_test,results)))


#tree.export_graphviz(clf,out_file='tree.pdf') 

features = vectorizor.get_feature_names()
#print(features)


dot_data = tree.export_graphviz(clf,
								feature_names=features,
                                out_file=None,
                                filled=True,
                                rounded=True)
								
graph = pydotplus.graph_from_dot_data(dot_data)


colors = ('turquoise', 'orange')
edges = collections.defaultdict(list)

for edge in graph.get_edge_list():
    edges[edge.get_source()].append(int(edge.get_destination()))

for edge in edges:
    edges[edge].sort()    
    for i in range(2):
        dest = graph.get_node(str(edges[edge][i]))[0]
        dest.set_fillcolor(colors[i])

graph.write_pdf('tree2.pdf')

end = time.time()
print(end - start)
