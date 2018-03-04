const mysql = require('mysql');
const connectionPool = require('../../../database');

const serverError = new Error(
    'An error occurred talking to the database'
);
serverError.status = 500;

const getConnection = () => {
    return new Promise((resolve, reject) => {
        connectionPool.getConnection((err, connection) => {
            if (err) {
                console.log('connection error', err);
                reject(serverError);
            }
            resolve(connection);
        });
    });
}

const queryDatabase = (connection, sqlQuery, keepConnection) => {
    return new Promise((resolve, reject) => {
        connection.query(sqlQuery, (error, results, fields) => {
            if (!keepConnection) {
                connection.release();
            }

            if (error) {
                console.log('query error', error);
                console.log(Object.keys(error));
                Object.keys(error).forEach((key) => {
                    console.log(`error[${key}]:`, error[key]);
                })
                reject(serverError);
            }
            resolve(results);
        });
    });
}

const userDatabase = {
    getAllUsers: () => {
        return getConnection()
            .then((connection) => {
                return queryDatabase(connection, 'SELECT * FROM user');
            });
    },

    getUserById: (id) => {
        return getConnection()
            .then((connection) => {
                const sqlQuery = mysql.format('SELECT * FROM user WHERE id = ?', id);
                console.log(sqlQuery);
                return queryDatabase(connection, sqlQuery);
            });
    },

    createUser: (user) => {
        return getConnection()
            .then((connection) => {
                // const sqlQuery = mysql.format('INSERT INTO user SET ?', user);
                const usernameQuery = mysql.format(
                    'SELECT * FROM user WHERE username = ?',
                    user.username
                );
                return queryDatabase(connection, usernameQuery);
            })
            .then((usernameResult) => {
                if (usernameResult) {
                    const error = new Error('Duplicate username');
                    error.status = 403;
                    throw error;
                }
            });
    }
};

module.exports = userDatabase;
