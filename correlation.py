import matplotlib as mpl
from matplotlib import pyplot
import dist_list_reader as dlr
import numpy as np

import partitions_generator as pg
import simulator as sim
from random import randint
import cvxpy as cp
import numpy as np

ALREADY_CALCULATED=False
DIGITS_PRECISION=10

def get_distribution(N):
	#setting up versus array
	if ALREADY_CALCULATED==True:
		return dlr.dist_list_reader()
	partitions=pg.partition_generator(N,5,0,N)
	#partitions=pg.partition_generator(N,5,0,int(float(2*N/5+1)))
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
	problem.solve();
	#printing distribution
	print("Probability distribution: ")
	distribution_list=[]
	for i in range(num):
		temp=(float)(dist[i].value)
		distribution_list.append((max(0,round(temp,DIGITS_PRECISION)),partitions[i]))
	distribution_list.sort(reverse=True)
	for a in distribution_list:
		print(a[1], " p= ", a[0])
	return distribution_list

def process_data(distribution_list,N): #returns pair_list of each two front combination mapped to its probability of occurring
	pair_list={};
	for i in range(N+1):
		for j in range(N+1):
			tp=(i,j)
			pair_list[tp]=0
	for i in range(len(distribution_list)):
		ps=distribution_list[i][1]
		prob=float(distribution_list[i][0])
		for a in range(5):
			for b in range(a+1,5):
				tp=(ps[a],ps[b])
				pair_list[tp]+=(float)(0.1*prob)
				if ps[a]!=ps[b]:
					tp2=(ps[b],ps[a])
					pair_list[tp2]+=(float)(0.1*prob)
	#optional for log based scaling
	for pair,val in pair_list.items():
		if val!=0:
			temp=float(1/np.log10(val))
			pair_list[pair]=-temp
	return pair_list

def process_smallest_two(distribution_list,N): #returns each val mapped to its probability of being the sum of two smallest values
	smallest_two_sum=[0 for i in range(N+1)]
	for a in distribution_list:
		smallest_two_sum[a[1][0]+a[1][1]]+=float(a[0])
	return smallest_two_sum

def process_any_two(pair_list,N):  #returns each val mapped to its probability of being the sum of two given fronts
	any_two_sum=[0 for i in range(N+1)]
	for pr,val in pair_list.items():
		curr=pr[0]+pr[1]
		if curr<=N:
			any_two_sum[curr]+=val
	return any_two_sum


def print_data(pair_list):
	for pair,val in pair_list.items():
		print(pair,":",val)


def plot_2D(plot_name,pair_list,N):
	zvals=[[pair_list[(x,y)] for x in range(N+1)] for y in range(N+1)]
	fig = pyplot.figure(2)
	cmap2 = mpl.colors.LinearSegmentedColormap.from_list('my_colormap',['white','black'],256)
	img2 = pyplot.imshow(zvals,interpolation='nearest',cmap = cmap2,origin='lower')
	pyplot.title(plot_name)
	pyplot.colorbar(img2,cmap=cmap2)
	pyplot.show()

def plot_1D(plot_name,sum_list,N):
	x=[i for i in range(N+1)]
	y=[sum_list[i] for i in range(N+1)]
	pyplot.plot(x,y, 'ro')
	pyplot.title(plot_name)
	pyplot.xticks(np.arange(min(x), max(x)+1, 2.0))
	#pyplot.axis([0, N, 0, 1.0])
	pyplot.show()

# def res(N):
# 	distribution_list=get_distribution(N)
# 	pair_list=process_data(distribution_list,N)
# 	smallest_two_sum=process_smallest_two(distribution_list,N)
# 	any_two_sum=process_any_two(pair_list,N)
# 	plot_1D("Sum of smallest two fronts",smallest_two_sum,N)
# 	plot_1D("Sum of any two fronts",any_two_sum,N)

def plot_smallest_two_sum(N):
	distribution_list=get_distribution(N)
	smallest_two_sum=process_smallest_two(distribution_list,N)
	plot_1D("Sum of smallest two fronts",smallest_two_sum,N)

def plot_any_two_sum(N):
	distribution_list=get_distribution(N)
	pair_list=process_data(distribution_list,N)
	any_two_sum=process_any_two(pair_list,N)
	plot_1D("Sum of any two fronts",any_two_sum,N)

def plot_any_two_ordered_pair(N):
	distribution_list=get_distribution(N)
	pair_list=process_data(distribution_list,N)
	plot_2D(N,pair_list,N)

plot_any_two_ordered_pair(31)






