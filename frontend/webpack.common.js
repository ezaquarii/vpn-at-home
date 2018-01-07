const merge = require('webpack-merge');
const path = require('path');


module.exports = {
    entry: ['./src/index.js'],
    output: {
        filename: 'static/bundle.js',
        publicPath: '/'
    },
    devtool: 'source-map',
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: 'babel-loader',
            },
            {
                test: /\.css$/,
                use: [
                    "style-loader",
                    "css-loader"
                ]
            },
            {
                test: /\.(woff2?|[ot]tf|eot|svg)$/,
                loader: 'file-loader',
                // Use publicPath ../, because this will be used in css files, and to reference a font from the fonts
                // folder in a css file in the styles folder the relative path is ../fonts/font-file.ext
                options: { name: 'static/fonts/[name].[hash].[ext]', publicPath: '../' }
            },
            {
                test: /\.(png|jpg)$/,
                loader: 'file-loader',
                options: {
                    name: 'static/[name].[hash].[ext]'
                }
            }
        ]
    }
};
