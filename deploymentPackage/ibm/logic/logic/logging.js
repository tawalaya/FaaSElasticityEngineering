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
        containerStartTime
    }
}