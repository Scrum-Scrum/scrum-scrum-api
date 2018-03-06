const bcrypt = require('bcryptjs');

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

const hashPassword = (password) => {
    return bcrypt.hashSync(password, 8);
};

// Replace `password` property with `hash` and the hashed password
const transformUser = (user) => {
    const { password, ...otherProps } = user;
    return { ...otherProps, hash: hashPassword(password) };
};

module.exports = {
    isValidUser,
    transformUser
};
