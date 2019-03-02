import cvxpy as cp
from math import factorial
from random import randint
import numpy as np

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
		counter=0;
		for i in range(3-a_wins,ties+1):
			counter=counter+binom(ties,i)
		return counter/(2**ties)

def get_probability(L1,L2):
	res=0
	for L in get_permutations(L2):
		res=res+get_results(L1,L)
	return res/120


#initialize arrays (partitions of 5)
a1=[0,0,0,0,5]
a2=[0,0,0,1,4]
a3=[0,0,0,2,3]
a4=[0,0,1,1,3]
a5=[0,0,1,2,2]
a6=[0,1,1,1,2]
a7=[1,1,1,1,1]
partitions=[a1,a2,a3,a4,a5,a6,a7]

p1=cp.Variable()
p2=cp.Variable()
p3=cp.Variable()
p4=cp.Variable()
p5=cp.Variable()
p6=cp.Variable()
p7=cp.Variable()


cn=[[0]*7 for i in range(7)]

for i in range(7):
	for j in range(7):
		cn[i][j]=get_probability(partitions[j],partitions[i])

x=(float)(input("Please enter p5: "))
y=(float)(input("Please enter p6: "))
z=(float)(input("Please enter p7: "))

answer=min([x*cn[i][4]+y*cn[i][5]+z*cn[i][6] for i in range(7)])
print("Best chance of winning is: ",answer)




# #get random vector to determine expression to be maximized
# dt=[0]*7
# for i in range(7):
# 	dt[i]=randint(1,2)

# objective=cp.Minimize(dt[0]*p1+dt[1]*p2+dt[2]*p3+dt[3]*p4+dt[4]*p5+dt[5]*p6+dt[6]*p7)
# constraints1=[p1*cn[i][0]+p2*cn[i][1]+p3*cn[i][2]+p4*cn[i][3]+p5*cn[i][4]+p6*cn[i][5]+p7*cn[i][6]>=0.5 for i in range(7)]
# constraints2=[p1>=0,p2>=0,p3>=0,p4>=0,p5>=0,p6>=0,p7>=0]
# constraints3=[p1+p2+p3+p4+p5+p6+p7==1]
# problem=cp.Problem(objective,constraints1+constraints2+constraints3)
# problem.solve()

# S=[p1.value,p2.value,p3.value,p4.value,p5.value,p6.value,p7.value]

# print("Minimizing: ",dt[0],"p1+",dt[1],"p2+",dt[2],"p3+",dt[3],"p4+",dt[4],"p5+",dt[5],"p6+",dt[6],"p7\n",sep='')

# print("Distribution: ")
# for i in range(7):
# 	temp=(float)(S[i])
# 	print(partitions[i]," p",i+1," = ",round(temp,3),sep='')
# print("Responses by Player Two --> Player One Probability of Win")
# for i in range(7):
# 	temp=0
# 	for j in range(7):
# 		temp=temp+((float)(S[j]))*cn[i][j]
# 	print(partitions[i], " --> ", round(temp,3))








