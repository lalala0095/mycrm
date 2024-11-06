const path = require('path');
const WorkboxWebpackPlugin = require('workbox-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');  // Add this import

const isProduction = process.env.NODE_ENV === 'production';

module.exports = (env, argv) => {
    const config = {
        entry: './src/main.js',  // Your main Vue entry point
        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: 'bundle.js',  // Output filename
        },
        module: {
            rules: [
              {
                test: /\.js$/,
                exclude: /node_modules/,
                use: 'babel-loader',  // Babel loader for JS files
              },
              {
                test: /\.vue$/,
                loader: 'vue-loader',  // For .vue file handling
              },
              {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],  // For CSS handling
              },
            ],
          },          
        plugins: [
            new (require('vue-loader').VueLoaderPlugin)(),  // Vue loader plugin for handling Vue components
            new HtmlWebpackPlugin({
                template: './public/index.html',  // Point to your HTML template
                inject: 'body',  // Inject the script tag into the body of the HTML
            }),
        ],
        resolve: {
            alias: {
                vue$: 'vue/dist/vue.esm-bundler.js',  // Ensure proper Vue resolution
            },
            extensions: ['.js', '.vue', '.json'],
        },
        devServer: {
            static: path.join(__dirname, 'dist'),  // Make sure static files are served from the dist folder
            open: true,
            historyApiFallback: true,  // For Vue Router with HTML5 history mode
            port: 8080,  // Default port for dev server
        },
    };

    // Conditional plugins and mode
    if (isProduction) {
        config.mode = 'production';
        config.plugins.push(new WorkboxWebpackPlugin.GenerateSW());  // For PWA support
    } else {
        config.mode = 'development';
    }

    return config;
};
