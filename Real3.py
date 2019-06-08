import partitions_generator as pg
from random import randint
import cvxpy as cp
import numpy as np

payoff=[3,-2,3,-2]

def getFirstThree(five):
	poss=[]
	for a in range(5):
		for b in range(1,5):
			for c in range(1,5):
				if b+c==5:
					continue;
				k1=a
				k2=(a+b)%5
				k3=(a+b+c)%5
				poss.append([five[k1],five[k2],five[k3]])
	return poss

def eval(three, t):
	wins=0
	ties=0
	# for i in range(3):
	# 	if three[i]>t[i]:
	# 		wins=wins+1
	for i in range(3):
		if three[i]>t[i]:
			wins+=1
		elif three[i]==t[i]:
			ties+=1
	if ties==0:
		return payoff[wins]
	elif ties==1:
		return 0.5*payoff[wins]+0.5*payoff[wins+1]
	elif ties==2:
		return 0.25*payoff[wins]+0.5*payoff[wins+1]+0.25*payoff[wins+2]
	else: #ties==3
		return payoff[wins]/8+3*payoff[wins+1]/8+3*payoff[wins+2]/8+payoff[wins+3]/8

def getResults(three,five):
	res=0
	poss=getFirstThree(five)
	for t in poss:
		res+=eval(three,t)
	return res/60


def solve(N):
	three=[]
	for blah in pg.three_front_generator(N):
		if blah[2]<=2*N/5+1:
			three.append(blah)
	#three=pg.three_front_generator(N)
	five=pg.partition_generator(N,5,0,N)
	num3=len(three)
	num5=len(five)
	dist=[0]*num3
	for i in range(num3):
		dist[i]=cp.Variable()
	res=[[0]*num5 for i in range(num3)]
	for i in range(num3):
		for j in range(num5):
			res[i][j]=getResults(three[i],five[j])
	w=cp.Variable()
	constraint1=[sum(dist)==1]
	constraint2=[sum(dist[i]*(three[i][0]+three[i][1]+three[i][2]) for i in range(num3))==0.6*N]
	constraint3=[dist[i]>=0 for i in range(num3)]
	constraint4=[sum(res[i][j]*dist[i] for i in range(num3))>=w for j in range(num5)]
	#E[x]=E[x^2]+4E[xy]
	constraint5=[sum(dist[i]*(three[i][0]+three[i][1]+three[i][2])/(3*N) for i in range(num3))==sum(dist[i]*(three[i][0]**2+three[i][1]**2+three[i][2]**2)/(3*N**2) for i in range(num3))+4*sum(dist[i]*(three[i][0]*three[i][1]+three[i][0]*three[i][2]+three[i][1]*three[i][2])/(3*N**2) for i in range(num3))]
	
	#E[x^2]=E[x^3]+4E[x^2y]
	constraint6=[sum(dist[i]*(three[i][0]**2+three[i][1]**2+three[i][2]**2)/(3*N**2) for i in range(num3))==sum(dist[i]*(three[i][0]**3+three[i][1]**3+three[i][2]**3)/(3*N**3) for i in range(num3))+4*sum(dist[i]*(three[i][0]**2*three[i][1]+three[i][0]**2*three[i][2]+three[i][1]**2*three[i][0]+three[i][1]**2*three[i][2]+three[i][2]**2*(three[i][0]+three[i][1]))/(6*N**3) for i in range(num3))]
	
	#E[xy]=2E[x^2y]+3E[xyz]
	constraint7=[sum(dist[i]*(three[i][0]*three[i][1]+three[i][0]*three[i][2]+three[i][1]*three[i][2])/(3*N**2) for i in range(num3))==2*sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]+three[i][1])+three[i][0]*three[i][2]*(three[i][0]+three[i][2])+three[i][1]*three[i][2]*(three[i][1]+three[i][2]))/(6*N**3) for i in range(num3))+3*sum(dist[i]*(three[i][0]*three[i][1]*three[i][2])/N**3 for i in range(num3))]
	
	#E[x^3]=E[x^4]+4E[x^3y]
	constraint8=[sum(dist[i]*(three[i][0]**3+three[i][1]**3+three[i][2]**3)/(3*N**3) for i in range(num3))==sum(dist[i]*(three[i][0]**4+three[i][1]**4+three[i][2]**4)/(3*N**4) for i in range(num3))+4*sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]**2+three[i][1]**2)+three[i][0]*three[i][2]*(three[i][0]**2+three[i][2]**2)+three[i][1]*three[i][2]*(three[i][1]**2+three[i][2]**2))/(6*N**4) for i in range(num3))]
	
	#E[x^2y]=E[x^3y]+E[x^2y^2]+3E[x^2yz]
	constraint9=[sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]+three[i][1])+three[i][0]*three[i][2]*(three[i][0]+three[i][2])+three[i][1]*three[i][2]*(three[i][1]+three[i][2]))/(6*N**3) for i in range(num3))==sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]**2+three[i][1]**2)+three[i][0]*three[i][2]*(three[i][0]**2+three[i][2]**2)+three[i][1]*three[i][2]*(three[i][1]**2+three[i][2]**2))/(6*N**4) for i in range(num3))+sum(dist[i]*(three[i][0]**2*three[i][1]**2+three[i][1]**2*three[i][2]**2+three[i][0]**2*three[i][2]**2)/(3*N**4) for i in range(num3))+3*sum(dist[i]*(three[i][0]*three[i][1]*three[i][2]*(three[i][0]+three[i][1]+three[i][2]))/(3*N**4) for i in range(num3))]

	objective=cp.Maximize(w)
	problem=cp.Problem(objective,constraint1+constraint2+constraint3+constraint4+constraint5+constraint6+constraint7+constraint8+constraint9)
	problem.solve(solver=cp.ECOS)
	print(problem.value)
	distribution_list=[]
	for i in range(num3):
		temp=(float)(dist[i].value)
		distribution_list.append((max(0,round(temp,4)),three[i]))
	distribution_list.sort(reverse=True)
	counter=0
	for a in distribution_list:
		counter=counter+1
		print(counter,". ",a[1], " p= ", a[0],sep='')

solve(10)

