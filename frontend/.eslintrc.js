module.exports = {
    root: true,
    env: {
        node: true,
        es6: true
    },
    extends: [
        'eslint:recommended',
        'plugin:vue/essential',
        '@vue/standard'
    ],
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
        'indent': ['error', 4],
        'semi': ['error', 'always'],
        'padded-blocks': ['error', { classes: 'always' }]
    },
    parserOptions: {
        parser: 'babel-eslint',
        ecmaFeatures: {
            legacyDecorators: true
        }
    }
};
