import partitions_generator as pg
from random import randint
import cvxpy as cp
import numpy as np
import simulator as sim

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

def getContribution(three,five):
	res=0
	for a in range(5):
		for b in range(a+1,5):
			for c in range(b+1,5):
				if (five[a]==three[0] and five[b]==three[1] and five[c]==three[2]):
					res+=(1/10)
	return res

def printDist(dist):
	print("PRINTING DIST")
	L=[]
	for a in dist: 
		L.append(a.value)
	L.sort(reverse=True)
	for a in L:
		print(a)


def getMoment(N,a,b,c,three,dist):
	res=0
	for i in range(len(three)):
		curr=three[i]
		for currP in sim.get_permutations(curr):
			res+=dist[i]*(currP[0]**a*currP[1]**b*currP[2]**c)/(6*N**(a+b+c))
	return res

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


	#Settng up the problem		
	w=cp.Variable()
	constraintList=[]
	constraint1=[sum(dist)==1]
	constraint2=[sum(dist[i]*(three[i][0]+three[i][1]+three[i][2]) for i in range(num3))==0.6*N]
	constraint3=[dist[i]>=0 for i in range(num3)]
	constraint4=[sum(res[i][j]*dist[i] for i in range(num3))>=w for j in range(num5)]
	#E[x]=E[x^2]+4E[xy]
	#constraint5=[sum(dist[i]*(three[i][0]+three[i][1]+three[i][2])/(3*N) for i in range(num3))==sum(dist[i]*(three[i][0]**2+three[i][1]**2+three[i][2]**2)/(3*N**2) for i in range(num3))+4*sum(dist[i]*(three[i][0]*three[i][1]+three[i][0]*three[i][2]+three[i][1]*three[i][2])/(3*N**2) for i in range(num3))]
	constraint5=[getMoment(N,1,0,0,three,dist)==getMoment(N,2,0,0,three,dist)+4*getMoment(N,1,1,0,three,dist)]
	#E[x^2]=E[x^3]+4E[x^2y]
	#constraint6=[sum(dist[i]*(three[i][0]**2+three[i][1]**2+three[i][2]**2)/(3*N**2) for i in range(num3))==sum(dist[i]*(three[i][0]**3+three[i][1]**3+three[i][2]**3)/(3*N**3) for i in range(num3))+4*sum(dist[i]*(three[i][0]**2*three[i][1]+three[i][0]**2*three[i][2]+three[i][1]**2*three[i][0]+three[i][1]**2*three[i][2]+three[i][2]**2*(three[i][0]+three[i][1]))/(6*N**3) for i in range(num3))]
	constraint6=[getMoment(N,2,0,0,three,dist)==getMoment(N,3,0,0,three,dist)+4*getMoment(N,2,1,0,three,dist)]
	#E[xy]=2E[x^2y]+3E[xyz]
	#constraint7=[sum(dist[i]*(three[i][0]*three[i][1]+three[i][0]*three[i][2]+three[i][1]*three[i][2])/(3*N**2) for i in range(num3))==2*sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]+three[i][1])+three[i][0]*three[i][2]*(three[i][0]+three[i][2])+three[i][1]*three[i][2]*(three[i][1]+three[i][2]))/(6*N**3) for i in range(num3))+3*sum(dist[i]*(three[i][0]*three[i][1]*three[i][2])/N**3 for i in range(num3))]
	constraint7=[getMoment(N,1,1,0,three,dist)==2*getMoment(N,2,1,0,three,dist)+3*getMoment(N,1,1,1,three,dist)]

	#E[x^3]=E[x^4]+4E[x^3y]
	#constraint8=[sum(dist[i]*(three[i][0]**3+three[i][1]**3+three[i][2]**3)/(3*N**3) for i in range(num3))==sum(dist[i]*(three[i][0]**4+three[i][1]**4+three[i][2]**4)/(3*N**4) for i in range(num3))+4*sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]**2+three[i][1]**2)+three[i][0]*three[i][2]*(three[i][0]**2+three[i][2]**2)+three[i][1]*three[i][2]*(three[i][1]**2+three[i][2]**2))/(6*N**4) for i in range(num3))]
	constraint8=[getMoment(N,3,0,0,three,dist)==getMoment(N,4,0,0,three,dist)+4*getMoment(N,3,1,0,three,dist)]
	#E[x^2y]=E[x^3y]+E[x^2y^2]+3E[x^2yz]
	#constraint9=[sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]+three[i][1])+three[i][0]*three[i][2]*(three[i][0]+three[i][2])+three[i][1]*three[i][2]*(three[i][1]+three[i][2]))/(6*N**3) for i in range(num3))==sum(dist[i]*(three[i][0]*three[i][1]*(three[i][0]**2+three[i][1]**2)+three[i][0]*three[i][2]*(three[i][0]**2+three[i][2]**2)+three[i][1]*three[i][2]*(three[i][1]**2+three[i][2]**2))/(6*N**4) for i in range(num3))+sum(dist[i]*(three[i][0]**2*three[i][1]**2+three[i][1]**2*three[i][2]**2+three[i][0]**2*three[i][2]**2)/(3*N**4) for i in range(num3))+3*sum(dist[i]*(three[i][0]*three[i][1]*three[i][2]*(three[i][0]+three[i][1]+three[i][2]))/(3*N**4) for i in range(num3))]
	constraint9=[getMoment(N,2,1,0,three,dist)==getMoment(N,3,1,0,three,dist)+getMoment(N,2,2,0,three,dist)+3*getMoment(N,2,1,1,three,dist)]

	constraintList+=constraint1
	constraintList+=constraint2
	constraintList+=constraint3
	constraintList+=constraint4
	constraintList+=constraint5
	constraintList+=constraint6
	constraintList+=constraint7
	constraintList+=constraint8
	constraintList+=constraint9

	objective=cp.Maximize(w)
	problem=cp.Problem(objective,constraintList)#constraint1+constraint2+constraint3+constraint4+constraint5+constraint6+constraint7+constraint8+constraint9)
	problem.solve(solver=cp.ECOS)
	#Printing results
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
	CONSTdist=[0]*num3
	for i in range(num3):
		CONSTdist[i]=dist[i].value





	#Consructing a five front distribution that best models this three front distribution
	contributionMatrix=[[0]*num5 for i in range(num3)]
	for i in range(num3):
		for j in range(num5):
			contributionMatrix[i][j]=getContribution(three[i],five[j])
	cn=[[0]*num5 for i in range(num5)]
	for i in range(num5):
		for j in range(num5):
			cn[i][j]=sim.get_probability(five[j],five[i])
	constraintList2=[]
	maxDiff=cp.Variable()
	dist2=[0]*num5
	for i in range(num5):
		dist2[i]=cp.Variable()

	#old constraints
	Constraint1=[sum([dist2[j]*cn[i][j] for j in range(num5)])>=0.5 for i in range(num5)]
	Constraint2=[dist2[i]>=0 for i in range(num5)]
	Constraint3=[sum(dist2)==1]

	#new constraints
	#maxDiff should be positive
	Constraint4=[maxDiff>=0]
	#maximum absolute difference between a triplet from three front dist and extracted triplet from five front dist is maxDiff
	Constraint5=[sum(dist2[i]*contributionMatrix[j][i] for i in range(num5))-CONSTdist[j]<=maxDiff for j in range(num3)]
	Constraint6=[CONSTdist[j]-sum(dist2[i]*contributionMatrix[j][i] for i in range(num5))<=maxDiff for j in range(num3)]

	constraintList2+=Constraint1
	constraintList2+=Constraint2
	constraintList2+=Constraint3
	constraintList2+=Constraint4
	constraintList2+=Constraint5
	constraintList2+=Constraint6
	objective=cp.Minimize(maxDiff)
	problem=cp.Problem(objective,constraintList2)
	problem.solve(solver=cp.ECOS)
	print("maxDiff: ",problem.value)

	#printing data
	print("\nCorresponding Five Front Distribution")
	distribution_list=[]
	for i in range(num5):
		temp=(float)(dist2[i].value)
		distribution_list.append((max(0,round(temp,5)),five[i]))
	distribution_list.sort(reverse=True)
	counter=0
	for a in distribution_list:
		counter=counter+1
		print(counter,". ",a[1], " p= ", a[0],sep='')

	print("\nThree front distribution from above:")
	#sim.extract_three_tuples_from_known(N,distribution_list)
	for i in range(num3):
		val=round(sum(dist2[j].value*contributionMatrix[i][j] for j in range(num5)),4)
		print(three[i]," From distribution: ",val, "Should be: ", np.round(CONSTdist[i],4))

##OH, the second problem is treating dist as additional cp  variables

solve(15)

