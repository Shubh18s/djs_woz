import React from "react";
import Tree, { TreeUtils } from "react-collapsible-tree";

onSelection = (id) => {
  this.setState((state) => ({
    selected: id,
    items: TreeUtils.toggleItemsToId(state.items, id, state.selected),
  }));
};

const items = [
    {
        "0": {
          "id": "0",
          "name": "Item-1"
        },
        "1": {
          "id": "1",
          "name": "Item-1",
          "children": ["1-1", "1-2", "1-3"]
        },
        "1-1": {
          "id": "1-1",
          "name": "Item-1-1",
          "children": null
        },
        "1-2": {
          "id": "1-2",
          "name": "Item-1-2",
          "children": null
        },
        "1-3": {
          "id": "1-3",
          "name": "Item-1-3",
          "children": null
        }
      },
];

const topId= [0,1];

export default class script_tree extends React.Component {
  render() {
    return (
      <div>
        <Tree
          items={items} // items
          topIds={topIds} // array containing all top level item ids
          onSelection={this.onSelection} // function
          selection={0} // selection
          parentIcon={undefined} // icon for folder
          parentOpenIcon={undefined} // icon for folder open
          leafIcon={undefined} // icon for single file
        />
      </div>
    );
  }
}
