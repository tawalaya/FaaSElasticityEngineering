'use strict';

const logic = require("./logic")

module.exports.hello = async (event, context) => {
  const result = logic()
  return {
    statusCode: 200,
    body: JSON.stringify(result),
  };
};
