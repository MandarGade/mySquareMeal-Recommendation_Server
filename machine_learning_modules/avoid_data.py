new_list=['wontons',
'lemon chicken',
'pork loin',
'roasted pigs',
'salty duck eggs',
'salty fish',
'red bean',
'prawn',
'lobster',
'oyster',
'honey',
'potsticker',
'potato',
'cream',
'butter',
'ghee',
'white rice',
'basmati rice',
'all purpose flour']

foot_to_avoid=['jasmin rice','white rice', 'pasta', 'white bread', 'bagels', 'white flour','white flour tortillas','crackers ', 'pretzels', 'cookies', 'cakes', 'muffins', 'beef', 'pork', 'lamb','fried', 'breaded', 'bacon', 'hot dogs', 'deli meats', 'deep fried', 'whole milk', 'full fat','sugar syrup', ' preserves', 'pickles', 'sauerkraut', 'butter', 'lard', 'palm oil', 'cream', 'fries','doughnuts','croissants', 'agave nectar', 'soda', 'lemon chicken', 'wontons','pork loin', 'roasted pigs', 'salty duck eggs', 'salty fish', 'red bean', 'prawn', 'lobster', 'honey''potsticker','potato', 'cream', 'butter', 'ghee', 'basmati rice', 'all purpose flour']

print(len(foot_to_avoid))

for item in new_list:
	if item not in foot_to_avoid:
		foot_to_avoid.append(item)


def get_avoid_list():
	print(len(foot_to_avoid))


get_avoid_list()

print(foot_to_avoid)