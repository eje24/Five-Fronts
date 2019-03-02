from general_optimal_response import get_distribution

file=open("more_than_x.txt","a")

def more_than(N):
	distribution=get_distribution(N)
	mt=[0]*(N+1)

	file.write('N={0}\n'.format(N))

	for (part,p) in distribution.items():
		for i in range(5):
			for n in range(part[i]+1):
				mt[n]=mt[n]+p*0.2

	for i in range(N+1):
		file.write('Probability of assigning at least {0} troops to a front: {1} \n '.format(i,round(mt[i],4)))
	file.flush()

more_than(30)
more_than(35)

