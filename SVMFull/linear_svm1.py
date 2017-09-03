import numpy as np
from random import shuffle
'''
def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train):
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    for j in xrange(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:,j] = dW[:,j] + X[i].T
        dW[:,y[i]] = dW[:,y[i]]-X[i].T

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # Add regularization to the loss.
  loss += 0.5 * reg * np.sum(W * W)

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################

  dW = dW/num_train + reg*W 

  return loss, dW
'''

def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  num_train = X.shape[0]
  num_classes = W.shape[1]
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  scores = X.dot(W)
  correct_class_scores = scores[range(num_train), list(y)].reshape(-1,1)
  margins = np.maximum(0, scores - np.tile(correct_class_scores, (1,num_classes)) + 1)
  margins[range(num_train), list(y)] = 0      #These are the terms max(0,si - si +1) that should've been zero, because we don't consider the actual class
  #score while calculating margins for loss. That's why we set them to 0.
  loss = np.sum(margins)
  loss /= num_train
  # Add regularization to the loss.
  
  loss += 0.5 * reg * np.sum(W * W)

  coeff_matrix = np.zeros((num_train, num_classes))
  coeff_matrix[margins > 0] = 1                                #That's because all weights here are the positive ones and 
  coeff_matrix[range(num_train), list(y)] = 0                                 #all the weights here would have negative sign since they were being subtracted.
  coeff_matrix[range(num_train), list(y)] = -np.sum(coeff_matrix, axis=1)   #In my solution, I multiplied this matrix with -(c-1). c -> no. of classes. The same things!

  dW = (X.T).dot(coeff_matrix)                                               #Can't relate this with my solution. ==
  dW = dW/num_train + reg*W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
