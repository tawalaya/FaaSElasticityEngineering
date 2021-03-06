const csv = require("fast-csv")
const fs = require("fs")

const logErrors = false
module.exports = {
  onLoadingStarted: onLoadingStarted,
  logResult: logResult
};

var csvStream = csv.createWriteStream({ headers: true }),
writableStream = fs.createWriteStream(`result-${Date.now()}.csv`);

writableStream.on("finish", function() {
  console.log("DONE!");
});

csvStream.pipe(writableStream);

var csvTimeoutStream = csv.createWriteStream({ headers: true }),
writableTimeoutStream = fs.createWriteStream(`timeout-${Date.now()}.csv`);

writableTimeoutStream.on("finish", function() {
  console.log("DONE!");
});

csvTimeoutStream.pipe(writableTimeoutStream);

function onLoadingStarted(requestParams, context, ee, next) {
  requestParams.url = process.env.target_url
  context.startTime = Date.now()
  context.requestId = (context.startTime+Math.floor(Math.random() * 10000000)).toString(32).toUpperCase()

  let message = {}
  message.requestTime = context.startTime
  message.requestId = context.requestId
  csvTimeoutStream.write(message);
  
  return next(); // MUST be called for the scenario to continue
}

function logResult(requestParams, response, context, ee, next) {
  let message = {}
  if (response.statusCode < 300) {
    try {
      message = JSON.parse(response.body);
      message.statusCode = response.statusCode
    }
    catch (e) {
      console.error(response)
      console.error(e)
      console.error(response.body)
      throw e
    }
  }
  else {
    message.statusCode = response.statusCode
    if (logErrors) {
      console.log(`${response.statusCode}: ${response.body}`)
    }
  }
  message.requestResponseLatency = Date.now() - context.startTime;
  message.requestTime = context.startTime
  message.responseTime = Date.now()
  message.requestId = context.requestId

  csvStream.write(message);
  return next(); // MUST be called for the scenario to continue
}
