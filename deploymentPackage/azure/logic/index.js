const fs = require('fs');
const logger = require("./logging")
const prime = require("./prime")

module.exports = () => {
    logger.start()
    const number = Math.floor((Math.random() * 500000) + 10000000)
    prime(number)
    return logger.end()
}