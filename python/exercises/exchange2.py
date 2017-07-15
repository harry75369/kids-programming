def n_ways_to_exchange(money, changes):
	if money < 0:
		return 0
	if money == 0:
		return 1
	if len(changes) == 0:
		return 1
	used_change = changes[0]
	left_changes = changes[1:]
	return n_ways_to_exchange(money - used_change, left_changes) + n_ways_to_exchange(money, left_changes)

def generate_all_exchanges(changes):
	if len(changes) == 0:
		return [[]]
	exchanges_without_first_change = generate_all_exchanges(changes[1:])
	exchanges_with_first_change = [changes[:1] + exchange for exchange in exchanges_without_first_change]
	return exchanges_with_first_change + exchanges_without_first_change

def n_ways_to_exchange2(money, changes):
	n_ways = 0
	for exchanges in generate_all_exchanges(changes):
		if sum(exchanges) <= money:
			n_ways += 1
	return n_ways

def n_ways_to_exchange_within_loss(money, changes, loss):
	n_ways = 0
	for exchanges in generate_all_exchanges(changes):
		exchanged_money = sum(exchanges)
		if exchanged_money <= money and money - exchanged_money <= loss:
			n_ways += 1
	return n_ways

def generate_all_exchanges_using_binary(changes):

	def make_binary_array(i, n):
		i_array = []
		while i > 0:
			i_array.append(i % 2)
			i = i // 2
		while len(i_array) < n:
			i_array.append(0)
		i_array.reverse()
		return i_array

	def select_changes(changes, i_array):
		#print(i_array)
		selected_changes = []
		for index, change in enumerate(changes):
			if i_array[index] == 1:
				selected_changes.append(change)
		return selected_changes

	n = len(changes)
	a = []
	for i in range(2 ** n):
		a.append(select_changes(changes, make_binary_array(i, n)))
	return a

def n_ways_to_exchange3(money, changes):
	n_ways = 0
	for exchanges in generate_all_exchanges_using_binary(changes):
		if sum(exchanges) <= money:
			n_ways += 1
	return n_ways

def n_ways_to_exchange_within_loss3(money, changes, loss):
	n_ways = 0
	for exchanges in generate_all_exchanges_using_binary(changes):
		exchanged_money = sum(exchanges)
		if exchanged_money <= money and money - exchanged_money <= loss:
			n_ways += 1
	return n_ways

#print(n_ways_to_exchange(10, [])) # 1
#print(n_ways_to_exchange(10, [5])) # 2
#print(n_ways_to_exchange(10, [10])) # 2
#print(n_ways_to_exchange(10, [20])) # 1
#print(n_ways_to_exchange(10, [5, 5])) # 4
#print(n_ways_to_exchange(10, [4, 8])) # 3
#print(n_ways_to_exchange(100, [70, 60, 50, 35, 25, 10], [])) # 22
#print(n_ways_to_exchange2(100, [70, 60, 50, 35, 25, 10])) # 22
print(n_ways_to_exchange3(100, [70, 60, 50, 35, 25, 10])) # 22
#print(n_ways_to_exchange_within_loss(100, [70, 60, 50, 35, 25, 10], 30)) # 12
print(n_ways_to_exchange_within_loss3(100, [70, 60, 50, 35, 25, 10], 30)) # 12