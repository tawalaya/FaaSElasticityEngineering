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

const containerStartTime = Date.now()
const containerId = (containerStartTime+Math.floor(Math.random() * 10000000)).toString(32).toUpperCase()
//Adapted from github.com/wlloyduw/SAAF
function faas_fingerprint(){
    var vmId = process.platform;
    if (vmId == "win32" || vmId == "win64") {
        
        vmId = process.env["COMPUTERNAME"]
    } else  {
        vmId =  Math.floor((Date.now()/1000)-(fs.readFileSync("/proc/uptime").toString().split(" ")[0].split(".")[0])).toString(32).toUpperCase();
    }
    let fingerprint = {};
    fingerprint["vId"] = vmId;
    var key = process.env.AWS_LAMBDA_LOG_STREAM_NAME;
    if (key != null) {
        fingerprint["platform"] = "AWS";
        fingerprint["CId"] = key;
        fingerprint["region"] = process.env.AWS_REGION;

        var vmID = fs.readFileSync("/proc/self/cgroup").toString();
        var index = vmID.indexOf("sandbox-root");
        fingerprint["HId"] = vmID.substring(index + 13, index + 19);
        fingerprint["RAW"] = vmID;
    } else {
        key = process.env.X_GOOGLE_FUNCTION_NAME;
        if (key != null) {
            fingerprint["platform"] = "GCF";
            fingerprint["CId"] = containerId;
            fingerprint["region"] = process.env.X_GOOGLE_FUNCTION_REGION;
            fingerprint["HId"] = vmId;

        } else {
            key = process.env.__OW_ACTION_NAME;
            if (key != null) {
                fingerprint["platform"] = "ICF";
                fingerprint["CId"] = containerId;
                fingerprint["region"] = process.env.__OW_API_HOST;
                fingerprint["HId"] = fs.readFileSync("/sys/hypervisor/uuid").toString().trim();
                fingerprint["RAW"] = fingerprint["HId"];
            } else {
                key = process.env.WEBSITE_HOSTNAME;
                if (key != null) {
                    fingerprint["platform"] = "ACF";
                    fingerprint["CId"] = key;
                    fingerprint["region"] = process.env.REGION_NAME;
                    fingerprint["HId"] = process.env.COMPUTERNAME;
                    fingerprint["RAW"] = process.env.WEBSITE_INSTANCE_ID;
                    fingerprint["extras"] = process.env.MACHINEKEY_DecryptionKey;
                } else {
                    fingerprint["platform"] = "Unknown";
                    fingerprint["CId"] = containerId;
                    fingerprint["HId"] = vmId;
                    fingerprint["region"] = "Unknown";
                    fingerprint["RAW"] = "Unknown";
                }
            }
        }
    }
    return fingerprint;
}

//detect vm id based on either boot time or mac-address+hostname (should be VM unique in azure)
const fingerprint = faas_fingerprint();

const osType = process.platform
const nodeVersion = process.version


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
        containerId:fingerprint["CId"],
        containerStartTime,
        vmId:fingerprint["HId"],
        primeNumber,
        result,
        osType,
        nodeVersion,
        pName:fingerprint["platform"],
        vName:fingerprint["vId"],
        region:fingerprint["region"],
        cName:containerId,
        raw:fingerprint["RAW"],
        extras:fingerprint["extras"],
    }
}
