import json 

# adj_matrix = [[1,3,4], [2,2,2]]
# oneD_list = [(1, 'name1'), (2, 'name2'), (3, 'name3')]

def nodes(kw_w_pairs): 
	'''
		hello
		- hi!

		input: list of keyword-weight pairs [(kw, w), ...]
		output: a list of {id:, value:, label: }
	'''
	nodes = [] 
	for index, element in enumerate(kw_w_pairs): 

		label, freq = element[0], element[1]
		dic = {'id': index, 'value': freq, 'label': label}
		nodes.append(dic)
	return nodes

def edges(sim_mat): 
	'''
		input: 2D list of weights 
		output: a list of {from: index of word 1, to: index of word 2, value: }
	'''
	edges = [] 
	for row in range(len(sim_mat)): 
		for col in range(row+1, len(sim_mat[row])): 
			weight = sim_mat[row][col]
			dic = {'from': row, 'to': col, 'value': weight}
			edges.append(dic)
	return edges 

def generate_json_pair(kw_w_pairs, sim_mat):
	nodes_list = json.dumps(nodes(kw_w_pairs))
	edges_list = json.dumps(edges(sim_mat))

	return (nodes_list, edges_list)
