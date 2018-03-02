const connectionPool = require('../../../database');

const serverError = new Error(
    'An error occurred talking to the database'
);
serverError.status = 500;

const databaseUserAccessor = {
    getAllUsers: (callback) => {
        connectionPool.getConnection((err, connection) => {
            if (err) {
                callback(undefined, serverError);
            } else {
                connection.query('SELECT * FROM user', (error, results, fields) => {
                    connection.release();

                    if (error) {
                        callback(undefined, serverError);
                    }
                    callback(results);
                });
            }
        });
    }

};

module.exports = databaseUserAccessor;
