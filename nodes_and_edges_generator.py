import json 

adj_matrix = [[1,3,4], [2,2,2]]
oneD_list = [(1, 'name1'), (2, 'name2'), (3, 'name3')]

def edges(adj_matrix): 
	'''
		input: 2D list of weights 
		output: a list of {from: index of word 1, to: index of word 2, value: }
	'''
	edges = [] 
	for row in range(len(adj_matrix)): 
		for col in range(row+1, len(adj_matrix[row])): 
			weight = adj_matrix[row][col]
			dic = {'from': row, 'to': col, 'value': weight}
			edges.append(dic)
	return edges 

def nodes(oneD_list): 
	'''
		hello
	'''
	nodes = [] 
	for index, element in enumerate(oneD_list): 

		freq, label = element[0], element[1]
		dic = {'id': index, 'value': freq, 'label': label}
		nodes.append(dic)
	return nodes 

edges = edges(adj_matrix)
nodes = nodes(oneD_list)

def write_json(edges, nodes): 
	with open('edges.json', 'w') as edge: 
		json.dump(edges, edge)
	with open('nodes.json', 'w') as node: 
		json.dump(nodes, node)

