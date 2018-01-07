const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = merge(common, {
    output: {
        path: path.resolve('dist'),
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'OpenVPN@Home - Development',
            template: './src/index.html',
            filename: 'index.html',
            inject: 'body'
        })
    ]
});
