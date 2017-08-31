primes = sieve [2..]
  where sieve (x:xs) = x : (sieve (filter (\y -> 0 /= rem y x) xs))

nth n = head . drop n

main = do
  print $ nth 10000 primes
