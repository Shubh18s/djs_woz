// SortTree.jsx
import React from "react";
import SortableTree from "react-sortable-tree";
import "react-sortable-tree/style.css";

export default class SortTree extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      treeData: [{ title: "Chicken", children: [{ title: "Egg" }] }],
    };
  }

  render() {
    return (
      <div style={{ height: 400 }}>
        <SortableTree
          treeData={this.state.treeData}
          onChange={(treeData) => this.setState({ treeData })}
        />
      </div>
    );
  }
}
