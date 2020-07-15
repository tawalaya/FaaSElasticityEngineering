const logic = require("../logic")

//console.log(isPrime(2))
module.exports = async function (context) {
    const result = logic()
    return {
      body: result,
    };
}