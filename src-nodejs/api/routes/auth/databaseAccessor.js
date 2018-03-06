const mysql = require('mysql');
const getConnection = require('../../../database/connection');
const errors = require('../../../errors');
const bcrypt = require('bcryptjs');


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
                        reject(errors.serverError);
                    }
                    resolve(results);
                });
            });
        });
}

const getHash = (usernameOrEmail) => {
    const sqlQuery = mysql.format(
        'SELECT hash FROM user WHERE username = ? OR email = ?',
        [usernameOrEmail, usernameOrEmail]
    );
    console.log('get hash sqlQuery', sqlQuery);
    return queryDatabase(sqlQuery);
}

const authDatabase = {
    checkHash: (authData) => {
        console.log('in check hash');
        console.log('authData', authData);
        return new Promise((resolve, reject) => {
            if (!authData.usernameOrEmail || !authData.password) {
                reject(errors.badRequestError);
            } else {
                resolve(authData);
            }
        })
        .then((authData) => {
            return getHash(authData.usernameOrEmail);
        })
        .then((hash) => {
            console.log('checking hash to authenticate');
            console.log('hash', hash);
            if (Array.isArray(hash) && hash.length > 0) {
                hash = hash[0].hash;
                const authenticated = bcrypt.compareSync(authData.password, hash);
                return authenticated;
            } else {
                return false;
            }

        });
    }
};

module.exports = authDatabase;
