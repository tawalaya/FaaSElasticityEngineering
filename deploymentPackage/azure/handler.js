'use strict';

const logic = require("./logic")
/* eslint-disable no-param-reassign */

module.exports.hello = async function (context) {
  const result = logic()
  return {
    body: result,
  };
}