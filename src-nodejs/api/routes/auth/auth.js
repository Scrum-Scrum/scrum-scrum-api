const express = require('express');
const router = express.Router();
const authDatabase = require('./databaseAccessor');
const errors = require('../../../errors');
const { generateToken, verifyToken } = require('./token');

router.post('/login', (req, res, next) => {
    console.log('req.body', req.body);
    authDatabase.checkHash(req.body)
        .then((authenticated) => {
            console.log('did we get to authenticate?');
            if (authenticated) {
                return generateToken({ usernameOrEmail: req.body.usernameOrEmail });
            } else {
                throw errors.unauthorizedError;
            }
        })
        .then((token) => {
            res.json({ token });
        })
        .catch((error) => {
            console.log('setting the status again');
            res.status(error.status).json({
                error: {
                    message: error.message
                }
            });
        });
});

module.exports = router;
