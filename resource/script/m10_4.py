# m10_4.py
def is_prime(x):
    for i in range(2, x):
        if x % i == 0:
            return False
    return True

if __name__ == "__main__":
    from sys import argv
    print is_prime(int(argv[1]))
