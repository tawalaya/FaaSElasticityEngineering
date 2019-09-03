const Pool = require('threads').Pool;
const pool = new Pool();
const logger = require("../logic/logging")

function threadedPrime(input, done) {
    const isPrime = (number) => {
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
      
    const ans = isPrime(input)
    done(ans)
}
//console.log(isPrime(2))
module.exports = (cb) => {
    logger.start()
    const number = Math.floor((Math.random() * 500000) + 10000000)
    const job = pool.run(threadedPrime).send(number)
    job.on('done', function (isPrime, input) {
        cb(null, logger.end())
    })    
}