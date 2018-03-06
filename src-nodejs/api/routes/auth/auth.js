const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const authDatabase = require('./databaseAccessor');
const errors = require('../../../errors');

router.post('/login', (req, res, next) => {
    authDatabase.checkHash(req.body)
        .then((authenticated) => {
            console.log('did we get to authenticate?');
            if (authenticated) {
                res.status(200).json({message: 'auth successful'});
            } else {
                res.status(errors.unauthorizedError.status).json({
                    message: errors.unauthorizedError.message
                });
            }
        });
});

module.exports = router;
