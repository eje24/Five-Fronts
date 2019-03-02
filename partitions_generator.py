def partition_generator(N, size, threshhold):
	L=[]
	if size==1:
		if N>=threshhold:
			return [[N]]
	elif threshhold*size>N:
		return [];
	for i in range(threshhold,N):
		for par in partition_generator(N-i,size-1,i):
			L.append([i]+par)
	return L

