from math import factorial
import distributionReader as dr
import cvxpy as cp

#Partition and pure strategy generation functions
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
	if a<b:
		return 0
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


#Printing distribution given distribution list generated from distributionReader
def print_distribution(distribution_list):
	counter=0
	num=len(distribution_list)
	for a in distribution_list:
		counter=counter+1
		print(counter,". ",a[1], " p= ", a[0],sep='')



#Extracting three front distributions from a five front distribution
def getFirstThree(five):
	poss=[]
	for a in range(5):
		for b in range(5):
			for c in range(5):
				if not (a<b and b<c):
					continue
				poss.append([five[a],five[b],five[c]])
	return poss

def find_index(a,three):
	for i in range(len(three)):
		if three[i]==a:
			return i
	print("No index found!")

def extract_three_tuples(N):
	three=three_front_generator(N)
	num3=len(three)
	# print("Lenth of three: ",num3)
	# blah=0
	# for a in three:
	# 	print(blah,a,sep='')
	# 	blah=blah+1
	threeDist=[0]*num3
	distribution_list=dr.distributionReader(N)
	for a in distribution_list:
		p=a[0]
		five=a[1]
		for a in getFirstThree(five):
			id=find_index(a,three)
			threeDist[id]=threeDist[id]+p/10

	response_list=[]
	for i in range(num3):
		response_list.append((round(threeDist[i],3),three[i]))
	response_list.sort(reverse=True)
	for a in response_list:
		print(a[1]," ---> ", a[0])
	# counter=0
	# for i in range(num3):
	# 	counter=counter+1
	# 	print(counter,". ",three[i], " p= ", threeDist[i],sep='')


#Fetching previously computed five front distributions
def distributionReader(N):
	if N==20:
		with open('20.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list
	elif N==25:
		with open('25.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list
	elif N==30:
		with open('30.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list
	elif N==35:
		with open('35.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list
	elif N==40:
		with open('40.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list
	elif N==45:
		with open('45.txt') as f:
			distribution_list=[]
			for line in f:
				temp1=[float(x) for x in line.split()]
				temp2=[int(temp1[i]) for i in range(5)]
				prob=float(temp1[5])
				res=(prob,temp2)
				distribution_list.append(res)
			return distribution_list

