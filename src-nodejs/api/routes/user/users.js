const express = require('express');
const router = express.Router();
const userDatabase = require('./databaseAccessor');

// List all users
router.get('/', (req, res, next) => {
    userDatabase.getAllUsers()
        .then((users) => {
            res.status(200).json({
                user: users
            });
        })
        .catch((error) => {
            res.status(error.status).json({
                error: {
                    message: error.message
                }
            });
        });
});

router.get('/:id', (req, res, next) => {
    userDatabase.getUserById(req.params.id)
        .then((user) => {
            if (user) {
                res.status(200).json({
                    user
                });
            } else {
                const notFound = new Error('User not found');
                notFound.status = 404;
                res.status(notFound.status).json({
                    error: {
                        message: notFound.message
                    }
                })
            }
        })
        .catch((error) => {
            res.status(error.status).json({
                error: {
                    message: error.message
                }
            });
        });
});

router.post('/', (req, res) => {
    const user = req.body;
    userDatabase.createUser(user)
        .then((user) => {
            res.status(200).json({
                created: user
            });
        })
        .catch((error) => {
            res.status(error.status).json({
                error: {
                    message: error.message
                }
            });
        });
})

module.exports = router;
