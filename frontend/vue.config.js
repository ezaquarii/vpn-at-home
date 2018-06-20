module.exports = {
    baseUrl: '/',
    outputDir: 'dist',
    assetsDir: 'static',
    configureWebpack: {
        output: {
            filename: 'static/[name].js'
        }
    }
};
