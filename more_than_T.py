import partitions_generator as pg
import simulator as sim
from random import randint
import cvxpy as cp
import numpy as np

def get_distribution(N,T):
	partitions=pg.partition_generator(N,5,0,N)
	num=len(partitions)

	cn=[[0]*num for i in range(num)]

	for i in range(num):
		for j in range(num):
			cn[i][j]=sim.get_probability(partitions[j],partitions[i])

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

print("Maximizing probability that at least T troops are sent to a front for N=",30)
for i in range(12,15):
	ans=get_distribution(30,i)





