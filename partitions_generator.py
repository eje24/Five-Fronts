def partition_generator(N, size, lower,upper):
	L=[]
	if upper>N:
		upper=N
	if size==1:
		if N>=lower and N<=upper:
			return [[N]]
	elif lower*size>N or upper*size<N:
		return [];
	for i in range(lower,upper+1):
		for par in partition_generator(N-i,size-1,i,upper):
			L.append([i]+par)
	return L

def three_front_generator(N):
	L=[]
	for a in range(N+1):
		for b in range(a,N+1-a):
			for c in range(b,N+1-a-b):
				L.append([a,b,c])
	return L







