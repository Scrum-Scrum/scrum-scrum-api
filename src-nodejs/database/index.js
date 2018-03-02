const mysql = require('mysql');
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'scrum_scrum',
    connectionLimit: 100
});

module.exports = pool;
