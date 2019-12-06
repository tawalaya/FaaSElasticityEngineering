const fs = require('fs');
const os = require("os");
const exec = require('child_process').exec;

var boottime;



var result = {
    env: process.env,
    config: process.config,
    args: process.execArgv,
    pid: process.pid,
    ppid: process.ppid,
    uptime: os.uptime(),
    mem: os.totalmem(),
    network: os.networkInterfaces(),
    vmid:""
};



if (boottime) {

}

module.exports.hello = function (context) {
    context.res = {
        // status: 200, /* Defaults to 200 */
        body: JSON.stringify(result),
    };

    exec('wmic os get lastBootUpTime', (err, stdout, stderr) => {
        if (err) { console.log("failed") };
        boottime = stdout;
        var date = boottime.split('\n')[1].trim().split('.')[0];
        var vmid = Number(date).toString(32).toUpperCase();
        result.vmid = vmid;
        context.done();
    })

};