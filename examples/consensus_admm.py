import numpy as np
from cvxpy import *

m = 10
n = 5
np.random.seed(1)
A = np.random.randn(m, n)
b = np.random.randn(m)
# # Precondition A and b.
# for row in range(m):
#     A[row, :] /= norm(A[row, :]).value
# for col in range(n):
#     A[:, col] /= norm(A[:, col]).value

# b /= norm(b).value

from cvxpy import *
from multiprocessing import Pool

def prox(args):
    f, v = args
    f += (rho/2)*sum_squares(x - v)
    Problem(Minimize(f)).solve()
    return x.value

x = Variable(n)
prox_arg = Parameter(n)
gamma = Parameter(sign="positive")
gamma.value = 1
rho = Parameter(sign="positive")
rho.value = 1

# Initialize x, z, u.
funcs = [sum_squares(A*x - b),
         gamma*norm(x, 1)]
ui = [np.zeros((n, 1)) for func in funcs]
z = np.zeros((n, 1))
pool = Pool(2)
for i in range(100):
    # x update.
    prox_args = [-z + u for u in ui]
    xi = map(prox, zip(funcs, prox_args))
    # z update.
    ui_xi = [x_ + u for x_, u in zip(xi, ui)]
    z = sum(ui_xi)/len(ui_xi)
    # u update.
    ui = [u_x - z for u_x in ui_xi]

obj = sum_squares(A*x - b) + gamma*norm(x, 1)
prob = Problem(Minimize(obj))
result = prob.solve()
# print x.value
# print z
print "ADMM best", (sum_squares(A*z - b) + gamma*norm(z, 1)).value
print "ECOS best", obj.value
# Boolean least squares with prox.
