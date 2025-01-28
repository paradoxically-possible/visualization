def pascalTriangle(n):
    for i in range(n):
        for j in range(i + 1):
            print(nCr(i, j), end=" ")
        print()  # Pindah ke baris baru setelah setiap baris Pascal's Triangle

def nCr(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def factorial(num):
    if num == 0:
        return 1
    else:
        return num * factorial(num - 1)

# Meminta input dari pengguna
try:
    n = int(input("Pick a random number: "))
    if n <= 0:
        print("Please enter a positive number.")
    else:
        print(f"\nPascal's Triangle for n = {n}:\n")
        pascalTriangle(n)
except ValueError:
    print("Invalid input. Please enter a valid integer.")