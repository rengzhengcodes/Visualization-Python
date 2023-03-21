# Mapping 1
buffer 2 stores (A, B, Z)\
	for m in [0, 4)\
	for k in [0, 2)\
	for n in [0, 4)

buffer 1 stores (~~A~~, ~~B~~, Z)\
	for m in [0, 4)\
	for n in [0, 4)\
	par-for k in [0, 8)

buffer 0 stores (A, B, Z)\
	for m in [0, 1)\
	for n in [0, 1)\
	for k in [0, 1)


# Mapping 2
buffer 2 stores (A, B, Z)\
	for k in [0, 2)\
	for m in [0, 2)\
	for n in [0, 4)

buffer 1 stores (A, B, Z)\
	for m in [0, 8)\
	for n in [0, 4)\
	par-for k in [0, 8)

buffer 0 stores (A, B, Z)\
	for m in [0, 1)\
	for n in [0, 1)\
	for k in [0, 1)


# Mapping1 in comparison to Mapping2
buffer 2 stores (A, B, Z)\
	for **m** in [0, 4 ^)\
	for **k** in [0, 2)\
	for n in [0, 4)

buffer 1 stores (~~A~~, ~~B~~, Z)\
	for m in [0, 4 v)\
	for n in [0, 4)\
	par-for k in [0, 8)

buffer 0 stores (A, B, Z)\
	for m in [0, 1)\
	for n in [0, 1)\
	for k in [0, 1)


# Mapping2 in comparison to Mapping1
buffer 2 stores (A, B, Z)\
	for **k** in [0, 2 v)\
	for **m** in [0, 2)\
	for n in [0, 4)

buffer 1 stores (A, B, Z)\
	for m in [0, 8 ^)\
	for n in [0, 4)\
	par-for k in [0, 8)

buffer 0 stores (A, B, Z)\
	for m in [0, 1)\
	for n in [0, 1)\
	for k in [0, 1)


