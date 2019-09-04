const fs = require('fs');
const logger = require("./logging")
const prime = require("./prime")

module.exports = () => {
    logger.start()
    const number = Math.floor((Math.random() * 1000) + 7500000)
    var result = prime(number)
    return logger.end(number,result)
}