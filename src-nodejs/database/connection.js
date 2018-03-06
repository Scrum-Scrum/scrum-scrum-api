const mysql = require('mysql');
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'scrum_scrum',
    connectionLimit: 100
});

const getConnection = () => {
    return new Promise((resolve, reject) => {
        pool.getConnection((err, connection) => {
            if (err) {
                console.log('connection error', err);
                reject(serverError);
            }
            resolve(connection);
        });
    });
};

module.exports = getConnection;
