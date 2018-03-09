const jwt = require('jsonwebtoken');
const errors = require('../../../errors');

const generateToken = (userData) => {
    const options = { expiresIn: '60s' };
    return new Promise((resolve, reject) => {
        jwt.sign(userData, 'secret_key', options, (error, token) => {
            if (error) {
                reject(errors.serverError);
            }

            resolve(token);
        });
    });
}

const extractToken = (req) => {
    const bearerHeader = req.headers['authorization'];
    if (bearerHeader !== undefined) {
        const bearer = bearerHeader.split(' ');
        const token = bearer[1];
        return token;
    }
};

const verifyToken = (req) => {
    return new Promise((resolve, reject) => {
        const token = extractToken(req);

        jwt.verify(token, 'secret_key', (err, data) => {
            if (err) {
                reject(errors.invalidTokenError);
            }

            resolve(data);
        });
    });
};

module.exports = {
    generateToken,
    verifyToken
};
