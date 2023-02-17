const webpack = require('webpack');
const path = require('path');

const config = {
    // single entry point file for the output bundle
    entry : path.join(__dirname, 'webapp/static/jsx/index.jsx'),
    output : {
        path: path.join(__dirname, 'webapp/static/dist'),
        filename: 'bundle.js'
    },
    // Specify how to process each file before bundling
    module : {
        rules : [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                include: path.resolve(__dirname, "./webapp/static/jsx/"),
                use: {
                  loader: "babel-loader"
                }
            },
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                include: path.resolve(__dirname, "./webapp/static/jsx/"),
                use: 'babel-loader'
            },
            {
                test: /\.(s(a|c)ss)$/,
                include: path.resolve(__dirname, "./webapp/static/jsx/"),
                use: ['style-loader','css-loader', 'sass-loader']
             },
             {
                test: /\.(woff|woff2|eot|ttf|svg|jpg|png)$/,
                include: path.resolve(__dirname, "./webapp/static/jsx/"),
                use: {
                  loader: 'url-loader',
                },
          },
        ]
    },
    // Which files should Webpack should look to bundle 
    // that are referenced by import or require()
    resolve : {
        extensions: ['.js', '.jsx', '.css'],
        modules: [
            'node_modules'
          ]       
    },
    // externals: { react: "React", "react-dom": "ReactDOM" },
    watchOptions: {
        ignored: /node_modules/
      },
    // plugins: [
    //     new webpack.ProvidePlugin({
    //        "React": "react",
    //     }),
    // ],
};

module.exports = config;