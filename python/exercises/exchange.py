def n_ways_to_exchange(money, changes):
	if money < 0:
		return 0
	if money == 0:
		return 1
	if len(changes) == 0:
		return 0
	used_change = changes[0]
	left_changes = changes[1:]
	return n_ways_to_exchange(money - used_change, changes) + n_ways_to_exchange(money, left_changes) 

print(n_ways_to_exchange(100, [50, 10, 5, 1]))