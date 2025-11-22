
# Sample Fibonacci Task
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# Calculate 10th fibonacci number (55)
result = fib(10)
