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
};

const queryDatabase = (sqlQuery) => {
    return getConnection()
        .then((connection) => {
            return new Promise((resolve, reject) => {
                connection.query(sqlQuery, (error, results, fields) => {
                    connection.release();

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
        });
}

const isValidUser = (user) => {
    const {
        id,
        email,
        username,
        first_name,
        last_name,
        date_joined,
        is_active
    } = user;

    return (email && username && first_name && last_name) && !(id || date_joined || is_active);
};

const userDatabase = {
    getAllUsers: () => {
        return queryDatabase('SELECT * FROM user');
    },

    getUserById: (id) => {
        const sqlQuery = mysql.format('SELECT * FROM user WHERE id = ?', id);
        return queryDatabase(sqlQuery);
    },

    createUser: (user) => {
        console.log('this', this);
        if (!isValidUser(user)) {
            const error = new Error('Attempted to write read-only values');
            error.status = 404;
            throw error;
        }
        console.log('creating username query');
        const usernameQuery = mysql.format(
            'SELECT * FROM user WHERE username = ?',
            user.username
        );
        return queryDatabase(usernameQuery)
            .then((usernameResult) => {
                if (usernameResult.length > 0) {
                    console.log(usernameResult);
                    const error = new Error('Duplicate username');
                    error.status = 403;
                    throw error;
                } else {
                    console.log('creating email query');
                    const emailQuery = mysql.format('SELECT * FROM user WHERE email = ?', user.email);
                    return queryDatabase(emailQuery);
                }
            })
            .then((emailResult) => {
                if (emailResult.length > 0) {
                    const error = new Error('Duplicate email');
                    error.status = 403;
                    throw error;
                } else {
                    console.log('creating user');
                    const createUserQuery = mysql.format(
                        'INSERT INTO user SET ?',
                        user
                    );
                    return queryDatabase(createUserQuery);
                }
            })
            .then((results) => {
                const getUserQuery = mysql.format(
                    'SELECT * FROM user WHERE id = ?',
                    results.insertId
                );
                return queryDatabase(getUserQuery);
            });
    }
};

module.exports = userDatabase;
