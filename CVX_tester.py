import cvxpy as cp

a=cp.Variable();
b=cp.Variable();
c=cp.Variable();
objective=cp.Maximize(cp.entr(a)+cp.entr(b)+cp.entr(c))
constraint5=[a+b+c==1]
constraint1=[a+b==1]
constraint2=[0<=a]
constraint3=[0<=b]
constraint4=[0<=c]
problem=cp.Problem(objective,constraint1+constraint2+constraint3+constraint4+constraint5)
problem.solve()
print("a: ",a.value)
print("b: ",b.value)
print("c: ",c.value)