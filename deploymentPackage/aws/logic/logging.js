const fs = require('fs');

var vmId =  Math.round((Date.now()/1000)-(fs.readFileSync("/proc/uptime").toString().split(" ")[0].split(".")[0])).toString(32).toUpperCase();

const containerStartTime = Date.now()
const containerId = Math.floor(Math.random() * 10000000)

let startTime;
module.exports.start = () => {
    startTime = Date.now()
}
module.exports.end = () => {
    const executionEndTime = Date.now()
    return {
        executionStartTime: startTime,
        executionEndTime,
        executionLatency: executionEndTime - startTime,
        containerId,
        containerStartTime,
        vmId
    }
}