import partitions_generator as pg
import simulator as sim
from random import randint
import cvxpy as cp
import numpy as np

DIGITS_PRECISION=8

def get_distribution(N):
	#setting up versus array
	partitions=pg.partition_generator(N,5,0,N)
	num=len(partitions)
	cn=[[0]*num for i in range(num)]

	for i in range(num):
		for j in range(num):
			cn[i][j]=sim.get_probability(partitions[j],partitions[i])


	#setting up cvxpy 
	dist=[0]*num
	for i in range(num):
		dist[i]=cp.Variable()
	objective=cp.Maximize(sum(cp.entr(dist[i]) for i in range(len(partitions)))) #maximize entropy
	constraint1=[sum([dist[j]*cn[i][j] for j in range(num)])>=0.5 for i in range(num)]
	constraint2=[dist[i]>=0 for i in range(num)]
	constraint3=[sum(dist)==1]
	problem=cp.Problem(objective,constraint1+constraint2+constraint3)
	problem.solve(solver=cp.ECOS)
	#printing distribution
	print("Entropy: ",problem.value)
	print("Ratio entropy/log(n): ", problem.value/np.log(num))
	print("Probability distribution: ")
	distribution_list=[]
	for i in range(num):
		temp=(float)(dist[i].value)
		distribution_list.append((max(0,round(temp,DIGITS_PRECISION)),partitions[i]))
	distribution_list.sort(reverse=True)
	counter=0
	for a in distribution_list:
		counter=counter+1
		print(counter,". ",a[1], " p= ", a[0],sep='')
	
	print("Responses by Player Two --> Player One Probability of Win")
	response_list=[]
	for i in range(num):
		temp=0
		for j in range(num):
			temp=temp+((float)(dist[j].value))*cn[i][j]
		response_list.append((round(temp,3),partitions[i]))

	response_list.sort()
	for a in response_list:
		print(a[1]," ---> ", a[0])


def do_res(res):
	print("N=",res,sep='')
	get_distribution(res)






