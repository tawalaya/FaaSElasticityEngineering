const fs = require('fs');
const os = require("os");

function hashString(str){
	let hash = 0;
	for (let i = 0; i < str.length; i++) {
		hash += Math.pow(str.charCodeAt(i) * 31, str.length - i);
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash;
}

//detect vm id based on either boot time or mac-address+hostname (should be VM unique in azure)
var vmId = process.platform;
if (vmId == "win32" || vmId == "win64") {
    vmId =  os.networkInterfaces()["Ethernet 2"][0]["mac"]
        + "|" + os.hostname();
    vmId = hashString(vmId)
} else  {
    vmId =  Math.round((Date.now()/1000)-(fs.readFileSync("/proc/uptime").toString().split(" ")[0].split(".")[0])).toString(32).toUpperCase();
}

const osType = process.platform
const nodeVersion = process.version
const containerStartTime = Date.now()
const containerId = Math.floor(Math.random() * 10000000)

let startTime;
module.exports.start = () => {
    startTime = Date.now()
}
module.exports.end = (primeNumber,result) => {
    const executionEndTime = Date.now()
    return {
        executionStartTime: startTime,
        executionEndTime,
        executionLatency: executionEndTime - startTime,
        containerId,
        containerStartTime,
        vmId,
        primeNumber,
        result,
        osType,
        nodeVersion
    }
}