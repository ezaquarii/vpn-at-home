const merge = require('webpack-merge');
const common = require('./webpack.common.js');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = merge(common, {
    output: {
        path: path.resolve('../backend/openvpnathome/apps/frontend/'),
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'OpenVPN@Home',
            template: './src/index.html',
            filename: 'templates/index.html',
            inject: 'body'
        })
    ]
});
