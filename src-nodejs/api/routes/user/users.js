const express = require('express');
const router = express.Router();
const userDatabase = require('./databaseAccessor');

// List all users
router.get('/', (req, res, next) => {
    userDatabase.getAllUsers((data, error) => {
        if (error) {
            res.status(error.status).json({
                error: {
                    message: error.message
                }
            });
        } else {
            res.status(200).json(data);
        }
    });
});

module.exports = router;
