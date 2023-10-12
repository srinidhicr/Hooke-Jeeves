#WORKING CODE HOOKE JEEVES - FORMAT OUTPUT

import tkinter as tk
from tkinter import ttk
import sympy as sp

def check_optimum(n, exp, values):
    gradient = []
    v = 97
    for i in range(n):
        gradient.append(sp.diff(exp, chr(v)))
        v += 1

    for i in gradient:
        if subvalues(n, i, values) != 0:
            return 0
    return 1

def Pattern(n, A, X, exp):
    S = []
    for i in range(len(A)):
        S.append(A[i] - X[i])
    # print(S)
    lam = sp.symbols('L')
    temp = ""
    for i in range(len(S)):
        temp += 'L*' + str(S[i])
        if i != len(S) - 1:
            temp += '+'
    lst = temp.split('+')
    temp = ""
    for i in range(len(lst)):
        temp += (str(A[i]) + '+' + lst[i])
        if i != len(lst) - 1:
            temp += " , "
    t = temp.split(',')
    for i in range(len(t)):
        t[i] = sp.sympify(t[i])  # Convert t[i] to symbolic expression using sympify

    aft = subvalues(n, exp, t)
    # print("After : ", aft)
    dif = sp.diff(aft, lam)
 #   print(dif)
    lamb = sp.solve(dif)
  #  print(lamb)

    if len(lamb) == 0:
        print("No solution found for the derivative.")
        return

    res = []
    for i in t:
        res.append(i.subs(lam, lamb[0]))  # Use lamb[0] since solve returns a list of solutions
   # print("Next point: ", res)
    return res


def exploratory(n, exp, delta, start, i):
      v1 = subvalues(n,exp,start)
      s=start
      t1= list(start)
      t1[i] += delta[i]
      v2 = subvalues(n,exp,t1)
      t2= list(start)
      t2[i] -= delta[i]
      #print(t2)
      v3 = subvalues(n,exp,t2)
      #print(v1,v2,v3)
      if min(v1,v2,v3)==v1 :
        return start
      elif min(v1,v2,v3)==v2 :
        return t1
      else :
        return t2

def subvalues(n, exp, start):
    dt = {}
    v = 97
    for i in range(n):
        dt[chr(v)] = start[i]
        v += 1
    res = exp.subs(dt)
    return res

def run_optimization():
    n = int(n_vars_entry.get())
    expression = sp.sympify(expression_entry.get())
    start = [float(val) for val in start_values_entry.get().split(",")]
    deltas = [float(delta) for delta in deltas_entry.get().split(",")]

    A = start
    prev_optimum = None
    i = 0
    while True:
        
        improved = False  # Flag to check if there was any improvement
        for i in range(n):
            new_A = exploratory(n, expression, deltas, A, i)
            if subvalues(n, expression, new_A) < subvalues(n, expression, A):
                A = new_A
                improved = True
        if not improved:
            # If there's no improvement, break the loop
            prev_optimum = A
            break
        i += 1
        print("Iteration ", i)
        print("A - ", A)
        new_start = Pattern(n, A, start, expression)
        start = new_start[:]
        print("X - ", new_start)
        print("\n")
        if check_optimum(n, expression, new_start) == 1:
            prev_optimum = new_start
            break
        A = new_start
    result_optimum.set(", ".join([str(round(val, 2)) for val in prev_optimum]))
    result_value.set(str(subvalues(n, expression, prev_optimum)))

# Create the main window
root = tk.Tk()
root.title("Hook-Jeeves Optimization")
root.geometry("600x400")

# Create labels and input fields
n_vars_label = ttk.Label(root, text="Enter n-vars:")
n_vars_label.pack()
n_vars_entry = ttk.Entry(root)
n_vars_entry.pack()

expression_label = ttk.Label(root, text="Enter the expression:")
expression_label.pack()
expression_entry = ttk.Entry(root)
expression_entry.pack()

start_values_label = ttk.Label(root, text="Enter starting values (comma-separated):")
start_values_label.pack()
start_values_entry = ttk.Entry(root)
start_values_entry.pack()

deltas_label = ttk.Label(root, text="Enter deltas (comma-separated):")
deltas_label.pack()
deltas_entry = ttk.Entry(root)
deltas_entry.pack()

run_button = ttk.Button(root, text="Run Optimization", command=run_optimization)
run_button.pack()

result_A = tk.StringVar()
result_X = tk.StringVar()
result_optimum = tk.StringVar()
result_value = tk.StringVar()

"""
result_label_A = ttk.Label(root, text="A:")
result_label_A.pack()
result_display_A = ttk.Label(root, textvariable=result_A)
result_display_A.pack()

result_label_X = ttk.Label(root, text="X:")
result_label_X.pack()
result_display_X = ttk.Label(root, textvariable=result_X)
result_display_X.pack()
"""

result_label_optimum = ttk.Label(root, text="Optimum Solution:")
result_label_optimum.pack()
result_display_optimum = ttk.Label(root, textvariable=result_optimum)
result_display_optimum.pack()

result_label_value = ttk.Label(root, text="Optimum Value:")
result_label_value.pack()
result_display_value = ttk.Label(root, textvariable=result_value)
result_display_value.pack()

root.mainloop()

# a - b + 2*a**2 + 2*a*b +b**2
