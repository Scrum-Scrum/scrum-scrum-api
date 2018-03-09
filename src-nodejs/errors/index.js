const serverError = new Error('An error occurred talking to the database');
serverError.status = 500;

const forbiddenError = new Error('Forbidden');
forbiddenError.status = 403;

const unauthorizedError = new Error('Not authorized');
unauthorizedError.status = 401;

const invalidTokenError = new Error('Invalid or expired token');
invalidTokenError.status = 401;

const badRequestError = new Error('Bad request');
badRequestError.status = 404;

module.exports = {
    badRequestError,
    forbiddenError,
    invalidTokenError,
    serverError,
    unauthorizedError
};
