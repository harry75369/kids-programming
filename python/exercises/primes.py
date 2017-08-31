def primes(n):

    store = {}

    def calcPrimes(n):
        if n == 0:
            return 2
        elif n in store:
            return store[n]
        else:
            ps = [calcPrimes(i) for i in range(n)]
            np = ps[n-1]
            is_prime = False
            while not is_prime:
                is_prime = True
                np += 1
                for p in ps:
                    if np % p == 0:
                        is_prime = False
                        break
            store[n] = np
            return np

    return calcPrimes(n)

print(primes(10000))
