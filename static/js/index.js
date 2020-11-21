// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import NavBar from "./NavBar";
import ChatBox from "./chatBox";
import QueryTitle from "./QueryTitle";
import QuickMenu from "./QuickMenu";
import SortTree from "./SortTree";
import DTree from "./DTree";

// ReactDOM.render(<NavBar />, document.getElementById("navbar"));
// ReactDOM.render(<QueryTitle />, document.getElementById("queryTitle"));
// ReactDOM.render(<ChatBox />, document.getElementById("chatbox"));
ReactDOM.render(<QuickMenu />, document.getElementById("quickMenu"));
// ReactDOM.render(<App />, document.getElementById("treegraph"));
// ReactDOM.render(<SortTree />, document.getElementById("sorttree"));
ReactDOM.render(<DTree />, document.getElementById("dtree"));