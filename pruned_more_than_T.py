import partitions_generator as pg
from math import factorial
from random import randint
import cvxpy as cp
import numpy as np

N=12

#tie_resolver={(0,0):0.5,(1,1):0.5,(1,2):0.2,(2,1):0.8}
tie_resolver=[[0.5],[0,0.5,0.2],[0,0.8,0.5]]

def get_permutations(L):
	if len(L)==1:
		return [[L[0]]]
	result=[]
	for i in range(len(L)):
		for perm in get_permutations(L[:i]+L[i+1:]):
			temp=[L[i]]+perm
			result.append(temp)
	return result

def binom(a,b):
	return factorial(a)/factorial(b)/factorial(a-b)

def get_results(L1, L2):
	a_wins=0
	b_wins=0
	for i in range(5):
		if L1[i]>L2[i]:
			a_wins=a_wins+1
		elif L1[i]<L2[i]:
			b_wins=b_wins+1
	ties=5-a_wins-b_wins
	if a_wins>2:
		return 1
	elif b_wins>2:
		return 0
	else:
		try:
			return tie_resolver[a_wins][b_wins]
		except:
			print("error with tie_resolver")
		# counter=0;
		# for i in range(3-a_wins,ties+1):
		# 	counter=counter+binom(ties,i)
		# return counter/(2**ties)

def get_probability(L1,L2):
	res=0
	for L in get_permutations(L2):
		res=res+get_results(L1,L)
	return res/120

def get_distribution(N,T):
	partitions=pg.partition_generator(N,5,0,(int)(N/2))
	num=len(partitions)

	cn=[[0]*num for i in range(num)]

	for i in range(num):
		for j in range(num):
			cn[i][j]=get_probability(partitions[j],partitions[i])

	dist=[0]*num
	for i in range(num):
		dist[i]=cp.Variable()
	
	#Maximize probability of being at least X
	tlist=[0]*len(partitions);
	for i in range(len(partitions)):
		counter=0;
		for j in range(5):
			if partitions[i][j]>=T:
				counter=counter+1
		tlist[i]=(counter/5)
	objective=cp.Maximize(sum(dist[i]*tlist[i] for i in range(len(partitions)))) #maximize chance that more than a certain amount (T) is sent to a front
	constraint1=[sum([dist[j]*cn[i][j] for j in range(num)])>=0.5 for i in range(num)]
	constraint2=[dist[i]>=0 for i in range(num)]
	constraint3=[sum(dist)==1]
	problem=cp.Problem(objective,constraint1+constraint2+constraint3)
	problem.solve()

	optimal_distribution={tuple(partitions[i]): dist[i].value for i in range(num)}
	ans=(float)(problem.value)
	print("T=",T, "  --> ", round(ans,3))
	# distribution_list=[]
	# for i in range(num):
	# 	temp=(float)(dist[i].value)
	# 	distribution_list.append((round(temp,3),partitions[i]))
	# distribution_list.sort(reverse=True)
	# for a in distribution_list:
	# 	print(a[1], " p= ", a[0])



	# print("Responses by Player Two --> Player One Probability of Win")
	# response_list=[]
	# for i in range(num):
	# 	temp=0
	# 	for j in range(num):
	# 		temp=temp+((float)(dist[j].value))*cn[i][j]
	# 	response_list.append((round(temp,3),partitions[i]))

	# response_list.sort()
	# for a in response_list:
	# 	print(a[1]," ---> ", a[0])

	return optimal_distribution

print("Maximizing probability that at least T troops are sent to a front for N=",40)
for i in range(16,18):
	ans=get_distribution(40,i)





