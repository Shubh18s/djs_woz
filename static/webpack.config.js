const webpack = require("webpack");
const config = {
  entry: __dirname + "/js/index.js",
  output: {
    path: __dirname + "/dist",
    filename: "bundle.js",
  },
  resolve: {
    extensions: [".js", ".jsx", ".css"],
  },
  module: {
    rules: [
      { test: /\.css$/, use: "css-loader" },
      { test: /\.jsx?/, exclude: /node_modules/, use: "babel-loader" },
      { test: /\.svg$/, loader: "svg-inline-loader",
      },
    ],
  },
};
module.exports = config;
