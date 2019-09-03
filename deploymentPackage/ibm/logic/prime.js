function isPrime(number) {
  const noPrimes={};
  const numberSqrt = Math.sqrt(number);
  for (let i=2; i<=numberSqrt; i++) {
    if (noPrimes[i]) continue;
    let k=1;
    do {
      noPrimes[k*i] = true;
      k++;
    }
    while (k*i<=number);
  }
  return !noPrimes[number]
}

module.exports=isPrime
