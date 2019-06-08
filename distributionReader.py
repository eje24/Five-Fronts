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