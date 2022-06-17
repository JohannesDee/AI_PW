# -*- coding: utf-8 -*-
"""EARIN_Exercise_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n5oIusV7-LDp5ALniBXsarOta7Hx-ccF

# **EARIN EXERICISE #1**  
[*Deininger Johannes, Sasikumar Kolamannathodiyil Hari Shankar*]

### Assignment Description

In this exercise you will implement two methods – Gradient Descent method and Newton’s method
for function minimalization (please, be aware that the user should have a possibility to select which
method will be taken for function minimalization).

Your program should have a possibility to optimize two types of functions - F(x) = ax^3 + bx^2 + cx + d (where a, b, c, d are scalar numbers – all parameters are specified by the user) and G(x) = c + b'x + x'Ax (where c is a scalar number, b is a d-dimensional vector, and A is a positive-definite
matrix – all parameters are specified by the user).

The result of your solution is found solution x* and function value F(x*) or G(x*). It should be
possible to define starting point for the optimization procedure in two ways: either user can directly
provide initial vector (or scalar number in the case of function F(x) or its elements get generated
based on drawing numbers (one number in the case of function F(x) from a uniform distribution
defined for the range [low,high] (the range is defined by the user).

In the case of stopping conditions, your program should provide three possibilities:
1. Maximum number of iterations
2. Desired value F(x) or G(x) to reach (so the process is finished when F(x) <= value_to_reach / G(x) <= value_to_reach
3. Maximum computation time

Moreover, your program must provide batch/restart mode. It means that the optimization process
will be restarted n-times (n-defined by the user). In this mode, your program needs to calculate ntimes values x* and function value F(x*) or G(x*), then as the output mean values and standard
deviation are reported. This mode should work exactly in the same manner as manually (and
independently) running the optimization process for the same F(x) or G(x), function multiple
times. So, if the starting point is set for random generation, it changes for every run.

## Solution
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import math

def getInputs():
    # Use a breakpoint in the code line below to debug your script.
    A = []
    b = []
    factors = []
    dimension = []
    stopping_critereon = []
    limits = []

    print('Welcome: If you want to minimize F(x) select 1, for G(x) select 2:')  # Press Strg+F8 to toggle the breakpoint.
    objective_function = int(input())
    print(objective_function)

    if objective_function == 1:
        print('Please enter Parameters a,b,c,d')
        dimension = 1
        a = float(input())
        b = float(input())
        c = float(input())
        d = float(input())
        factors = [a,b,c,d]

    elif objective_function == 2:

        print('Please enter value of c (scalar)')
        c = float(input())
        print(c)
        print('Pease enter d-dimesional vector b, values separated by space')
        arr = input()  # takes the whole line of n numbers
        b = np.array([list(map(int, arr.split(' ')))]).T
        print(b)
        dimension = len(b)
        print("Please enter positive definite", dimension, " * " ,dimension, "Matrix A rowwise element-by-element separated by return'")
        cond1 = 0
        while cond1 == 0:
            A = []
            # For user input
            for i in range(dimension):  # A for loop for row entries
                g = []
                for j in range(dimension):  # A for loop for column entries
                    g.append(int(input()))
                A.append(g)
            print(A)
            if np.all(np.linalg.eigvals(A) > 0):
                print('Correct inputs')
                cond1 =1
            else:
                print("Matrix not positive-defite, reenter Matrix")
        print(A)
        A = np.array(A)
    else:
        print('error')

    print('Which algorith? Select 1 for Steepest Descent, 2 for Newton')
    algorithm = int(input())
    if algorithm == 1:
        print('You Selected Steepest Descent')
    if algorithm == 2:
        print('You selected Newton')


    print('If you want to define a starting point, press 1. For defining starting point range, press 2')
    starting_point = []
    start_select = int(input())
    if start_select == 1 and objective_function == 1:
        print("Enter the Starting Point")
        starting_point = int(input())
        print(starting_point)
    elif start_select == 1 and objective_function == 2:
        print("Enter a" , dimension ,"D Starting Point, separating dimensions by blank space")
        arr = input()  # takes the whole line of n numbers
        starting_point = np.array([list(map(int, arr.split(' ')))]).T
        print(starting_point)

    elif start_select == 2:
        print("Define lower limits for generating a starting point")
        lowerlim = int(input())
        print("Define upper limits for generating a starting point")
        upperlim = int(input())
        limits = [lowerlim, upperlim]
        print('Limits are:')
        print(limits)

    print("Which stopping criterion? Select 1 for number of iterations, 2 for desired value or 3 for computation time.")
    criterion = int(input())
    if criterion == 1:
        print("Enter max number of iterations")
        stopping_critereon = int(input())
    elif criterion == 2:
        print("Enter minimum value which should be reached:")
        stopping_critereon = float(input())
    elif criterion == 3:
        print("Enter max computation time in seconds")
        stopping_critereon = float(input())

    print("How many batches do you want to run?")
    batches = int(input())

    return objective_function, factors, c, b, A, algorithm, starting_point, criterion, stopping_critereon, batches, limits, dimension

def f(factors,x):
  return factors[0]*x*x*x + factors[1]*x*x + factors[2]*x +factors[3]

def g(c,b,A,x):
  return np.array(c + np.matmul(np.transpose(b),x) + np.matmul(np.matmul(np.transpose(x),A),x)).item()

def dt_f(factors,x):
  return 3*factors[0]*(x**2) + 2*factors[1]*x + factors[2]

def dt_g(b,A,x):
  return b + 2*np.matmul(A, x)

def dt2_f(factors,x):
  return 6*factors[0]*x +2*factors[1]

def dt2_g(b,A,x):
  return 2*A

def grad_descent(strt, criterion, stopping_criterion, obt_func, factors, c, b, A): 
  x_final = strt
  lr_final = 0
  if (obt_func == 1):
    y_final = f(factors, x_final)
  elif (obt_func == 2):
    y_final = g(c, b, A, x_final)
  lr_set = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3]
  for lr in lr_set:
    x = strt
    counter = 0
    start_time = time.perf_counter()
    while 1:
      counter = counter + 1
      if (obt_func == 1):
        y = f(factors, x)
        dt_y = dt_f(factors,x)
      elif (obt_func == 2):
        y = g(c, b, A, x)
        dt_y = dt_g(b,A,x)
      if criterion == 1 and counter >= stopping_criterion:
        if(y < y_final):
          x_final = x
          y_final = y
          lr_final = lr
        break
      if criterion == 2 and y < stopping_criterion:
        if(y < y_final):
          x_final = x
          y_final = y
          lr_final = lr
        break
      if criterion == 3 and time.perf_counter() - start_time > stopping_criterion:
        if(y < y_final):
          x_final = x
          y_final = y
          lr_final = lr
        break
      change = lr*dt_y
      x = x  - change 
  return x_final

def newton(strt, criterion, stopping_criterion,  obt_func, factors, b, A):
    x = strt
    start_time = time.perf_counter()
    counter = 0
    while 1:
        counter = counter +1
        if (obt_func == 1):
            y = f(factors, x)
            dt_y = dt_f(factors,x)
            dt2_y = dt2_f(factors, x)
        elif (obt_func == 2):
            y = g(c,b, A, x)
            dt_y = dt_g(b,A,x)
            dt2_y = dt2_g(b, A, x)
        if criterion == 1 and counter >= stopping_criterion:
            return x
        if criterion == 2 and y < stopping_criterion:
            return x
        if criterion == 3 and time.perf_counter() - start_time > stopping_criterion:
            return x
        
        if obt_func == 1:
         # print(x)
          if dt_y == 0:
              print('Zero derivative. No solution found.')
              return None
          if x == np.inf:
              print('At least 1 parameter is infinite')
              return (np.inf)
          if x == -np.inf:
              print('At least 1 parameter is infinite')
              return -np.inf
        else:
          if dt_y.all == 0:
            print('Zero derivative. No solution found.')
            return None
          if x.any == np.inf:
              print('At least 1 parameter is infinite')
              return (np.inf)
          if x.any == -np.inf:
              print('At least 1 parameter is infinite')
              return -np.inf
        if (obt_func == 1):
            step = - dt_y /dt2_y
            x = x + step

        elif (obt_func == 2):
            M = 0.5 * np.linalg.inv(dt2_y)
            step = - M.dot((dt_y)) # was transpose dt_y                   
            x = np.add(x, step)

print("Hello! Welcome to Minima Finder. Please follow the instructions to find the minima of the following functions")
print("1. ax^3 +bx^2 +cx + d")
print("2. c +b'x + x'Ax")

inputs = getInputs()

obt_func = inputs[0]
factors = inputs[1] 
c = inputs[2] 
b = inputs[3] 
A = inputs[4] 
algo = inputs[5] 
strt = inputs[6] 
criterion = inputs[7] 
stopping_criterion = inputs[8] 
batches = inputs[9]
limits = inputs[10]
dim = inputs[11]

if(len(limits)!=0):
  x_all = np.zeros(shape=(dim,1))
  for r in range(batches):
    x_start = np.random.uniform(low=limits[0], high=limits[1], size=(dim,1))
    if(algo == 1):
      x = np.array(grad_descent(x_start, criterion, stopping_criterion, obt_func, factors, c, b, A))
      if(obt_func == 1):
        print("x* of batch", r," is:", np.array(x).item(),"its value of f(x*) is", np.array(f(factors,x)).item())
      elif(obt_func == 2):
        print("x* of batch", r," is:", x,"its value of g(x*) is", g(c,b,A,x))
    elif(algo == 2):
      x = np.array(newton(x_start, criterion, stopping_criterion, obt_func, factors, b, A))
      if(obt_func == 1):
        print("x* of batch", r," is:", np.array(x).item(),"its value of f(x*) is", np.array(f(factors,x)).item())
      elif(obt_func == 2):
        print("x* of batch", r," is:", x,"its value of g(x*) is", g(c,b,A,x))
    if(r == 0):
      x_all = x
    else:
      x_all = np.concatenate((x_all,x),axis=1)
 # print(x_all)
  x_mean = (np.mean(x_all, axis=1)).T
  x_std =  (np.std(x_all, axis=1)).T
  if(obt_func == 1 and x):
    x_mean = np.array(x_mean).item()
    x_std = np.array(x_std).item()
    print("Mean and standard dev of x* all batches are:", x_mean,",",x_std, " and its value of f(x*) is", f(factors,x))
  elif(obt_func == 2 and x.any):
    print("Mean and standard dev of x* all batches are :", x_mean, ",",x_std, " and its value of g(x*) is", g(c,b,A,x))
else:
  if(algo == 1):
    x = np.array(grad_descent(strt, criterion, stopping_criterion, obt_func, factors, c, b, A))
  elif(algo == 2):
    x = np.array(newton(strt, criterion, stopping_criterion, obt_func, factors, b, A))
  if obt_func == 1 and x:
    print("Mean and standard dev x* are:", x,",0"," and its value of f(x*) is", f(factors,x))
  elif obt_func == 2 and x.any:
    print("Mean and standard dev x* are:", x,",0", "and its value of g(x*) is", g(c,b,A,x))