# As usual, a bit of setup

## =========================================================================== SECTION 1 ============================================================ ##

import time
import numpy as np
import matplotlib.pyplot as plt
from classifiers.fc_net import *
from data_utils import get_CIFAR10_data
from gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
from solver import Solver


plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


def rel_error(x, y):
  """ returns relative error """
  return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))



data = get_CIFAR10_data()
for k, v in data.items():              # =======changed this from data.iteritems() to data.items()
  print('%s: ' % k, v.shape)


# ================= Finally got rid of all the bugs upto this point!

##========================================================================= SECTION 2 ============================================================ ##

# Test the affine_forward function

num_inputs = 2
input_shape = (4, 5, 6)
output_dim = 3

input_size = num_inputs * np.prod(input_shape)
weight_size = output_dim * np.prod(input_shape)

x = np.linspace(-0.1, 0.5, num=input_size).reshape(num_inputs, *input_shape)
w = np.linspace(-0.2, 0.3, num=weight_size).reshape(np.prod(input_shape), output_dim)
b = np.linspace(-0.3, 0.1, num=output_dim)

out, _ = affine_forward(x, w, b)
correct_out = np.array([[ 1.49834967,  1.70660132,  1.91485297],
                        [ 3.25553199,  3.5141327,   3.77273342]])

# Compare your output with ours. The error should be around 1e-9.
print( 'Testing affine_forward function:')
print( 'difference: ', rel_error(out, correct_out))


## ======================================================================= SECTION 3 ============================================================== ##


# Test the affine_backward function

x = np.random.randn(10, 2, 3)
w = np.random.randn(6, 5)
b = np.random.randn(5)
dout = np.random.randn(10, 5)

dx_num = eval_numerical_gradient_array(lambda x: affine_forward(x, w, b)[0], x, dout)
dw_num = eval_numerical_gradient_array(lambda w: affine_forward(x, w, b)[0], w, dout)
db_num = eval_numerical_gradient_array(lambda b: affine_forward(x, w, b)[0], b, dout)

_, cache = affine_forward(x, w, b)
dx, dw, db = affine_backward(dout, cache)

# The error should be around 1e-10
print( 'Testing affine_backward function:')
print( 'dx error: ', rel_error(dx_num, dx))
print( 'dw error: ', rel_error(dw_num, dw))
print( 'db error: ', rel_error(db_num, db))

''' ==================================Error obtained with 49000 images in training set.
Testing affine_backward function:
dx error:  4.66026074929e-10
dw error:  1.57145125943e-10
db error:  3.74838319626e-12 '''



## ===================================================================== SECTION 4 ========================================================= ##


# Test the ReLu Forward function.

x = np.linspace(-0.5, 0.5, num=12).reshape(3, 4)

out, _ = relu_forward(x)
correct_out = np.array([[ 0.,          0.,          0.,          0.,        ],
                        [ 0.,          0.,          0.04545455,  0.13636364,],
                        [ 0.22727273,  0.31818182,  0.40909091,  0.5,       ]])

# Compare your output with ours. The error should be around 1e-8
print( 'Testing relu_forward function:')
print('difference: ', rel_error(out, correct_out))


## ====================================================================== SECTION 5 ====================================================== ##

# Test the ReLu Backward function

x = np.random.randn(10, 10)
dout = np.random.randn(*x.shape)

dx_num = eval_numerical_gradient_array(lambda x: relu_forward(x)[0], x, dout)

_, cache = relu_forward(x)
dx = relu_backward(dout, cache)

# The error should be around 1e-12
print( 'Testing relu_backward function:')
print( 'dx error: ', rel_error(dx_num, dx))


## ===================================================================== SECTION 6 ======================================================= ##

## take a look at the affine_relu_forward and affine_relu_backward functions, and run the following to numerically gradient check the backward pass

from cs231n.layer_utils import affine_relu_forward, affine_relu_backward

x = np.random.randn(2, 3, 4)
w = np.random.randn(12, 10)
b = np.random.randn(10)
dout = np.random.randn(2, 10)

out, cache = affine_relu_forward(x, w, b)
dx, dw, db = affine_relu_backward(dout, cache)

dx_num = eval_numerical_gradient_array(lambda x: affine_relu_forward(x, w, b)[0], x, dout)
dw_num = eval_numerical_gradient_array(lambda w: affine_relu_forward(x, w, b)[0], w, dout)
db_num = eval_numerical_gradient_array(lambda b: affine_relu_forward(x, w, b)[0], b, dout)

print( 'Testing affine_relu_forward:')
print( 'dx error: ', rel_error(dx_num, dx) )
print( 'dw error: ', rel_error(dw_num, dw) )
print( 'db error: ', rel_error(db_num, db) )

## ================




































