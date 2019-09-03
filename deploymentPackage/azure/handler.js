'use strict';

const logic = require("./multithreadedLogic")
/* eslint-disable no-param-reassign */

module.exports.hello = function (context) {
  logic((err, ans) => {
    context.res = {
      // status: 200, /* Defaults to 200 */
      body: JSON.stringify(ans),
    };
    context.done();
  })
  
};