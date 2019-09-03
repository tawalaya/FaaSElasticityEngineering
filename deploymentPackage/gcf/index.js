
const logic = require("./logic")
exports.http = (request, response) => {
    response.status(200).send(logic())
};
