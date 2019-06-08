def dist_list_reader():
	with open('staging.txt') as f:
		distribution_list=[]
		for line in f:
			temp1=[float(x) for x in line.split()]
			temp2=[int(temp1[i]) for i in range(5)]
			prob=float(temp1[5])
			res=(prob,temp2)
			distribution_list.append(res)
		return distribution_list
