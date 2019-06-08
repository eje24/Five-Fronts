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

def get_distribution(N,exp,opt):
	partitions=pg.partition_generator(N,5,0,N)
	num=len(partitions)

	cn=[[0]*num for i in range(num)]

	for i in range(num):
		for j in range(num):
			cn[i][j]=get_probability(partitions[j],partitions[i])

	dist=[0]*num
	for i in range(num):
		dist[i]=cp.Variable()
	
	#Maximize probability of being at least X
	one_list=[0]*len(partitions);
	two_list=[0]*len(partitions);
	three_list=[0]*len(partitions);
	four_list=[0]*len(partitions);
	blah_list=[one_list,two_list,three_list,four_list]
	for i in range(len(partitions)):
		for j in range(5):
			for e in range(4):
				blah_list[e][i]=blah_list[e][i]+(partitions[i][j]**(e+1))/5
	if opt==0:
		objective=cp.Minimize(sum(dist[i]*blah_list[exp][i] for i in range(len(partitions)))) #maximize chance that more than a certain amount (T) is sent to a front
	elif opt==1:
		objective=cp.Maximize(sum(dist[i]*blah_list[exp][i] for i in range(len(partitions))))
	constraint1=[sum([dist[j]*cn[i][j] for j in range(num)])>=0.5 for i in range(num)]
	constraint2=[dist[i]>=0 for i in range(num)]
	constraint3=[sum(dist)==1]
	problem=cp.Problem(objective,constraint1+constraint2+constraint3)
	problem.solve()

	optimal_distribution={tuple(partitions[i]): dist[i].value for i in range(num)}
	ans=(float)(problem.value)
	x1=sum(dist[i].value*blah_list[0][i] for i in range(len(partitions)))
	x2=sum(dist[i].value*blah_list[1][i] for i in range(len(partitions)))
	x3=sum(dist[i].value*blah_list[2][i] for i in range(len(partitions)))
	x4=sum(dist[i].value*blah_list[3][i] for i in range(len(partitions)))
	x1=round(x1,3)
	x2=round(x2,3)
	x3=round(x3,3)
	x4=round(x4,3);
	print("Expected value of x: ",x1)
	print("Expected value of x^2: ",x2)
	print("Expected value of x^3: ",x3)
	print("Expected value of x^4: ", x4)
	distribution_list=[]
	for i in range(num):
		temp=(float)(dist[i].value)
		if temp>0.000001:
			distribution_list.append((round(temp,3),partitions[i]))
	distribution_list.sort(reverse=True)
	for a in distribution_list:
		print(a[1], " p= ", a[0])

	return optimal_distribution

N=20
print("N=20")
for i in range(1,2):
	print("Minimizing E[x^",i+1,"]",sep='')
	get_distribution(N,i,0);
for i in range(1,2):
	print("Maximizing E[x^",i+1,"]",sep='')
	get_distribution(N,i,1)






