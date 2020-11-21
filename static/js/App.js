// App.jsx
import React from "react";
import Tree from "react-tree-graph";
import "react-tree-graph/dist/style.css";
let data = {
  name: "Should gay marriage be legal in Australia?",
  children: [
    {
      name: "Found 2 pros and 3 cons. Would you like to hear them?",
    },
    {
      name: "Child Two",
    },
  ],
};
export default class App extends React.Component {
  render() {
    return (
      <div>
        <Tree data={data} height={800} width={800} />
      </div>
    );
  }
}
