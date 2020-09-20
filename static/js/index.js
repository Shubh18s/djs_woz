// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import NavBar from "./NavBar";
import ChatBox from "./chatBox";
import QueryTitle from "./QueryTitle";

ReactDOM.render(<QueryTitle />, document.getElementById("hello"));
ReactDOM.render(<NavBar />, document.getElementById("navbar"));
ReactDOM.render(<QueryTitle />, document.getElementById("queryTitle"));
ReactDOM.render(<ChatBox />, document.getElementById("chatbox"));