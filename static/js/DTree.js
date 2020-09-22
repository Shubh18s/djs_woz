import React from "react";
import Tree from "react-d3-tree";

const myTreeData = [
  {
    name: "Found 2 Pros and 3 Cons. Would you like to hear them?",
    attributes: {
      
    },
    nodeSvgShape: {
        shape: 'rect',
        shapeProps: {
          width: 20,
          height: 20,
          x: -10,
          y: -10,
          fill: 'red',
        },
      },
    
    children: [
      {
        name: "Yes! I would like to hear more Pros.",
        attributes: {
          
        },
        nodeSvgShape: {
            shape: 'rect',
            shapeProps: {
              width: 20,
              height: 20,
              x: -10,
              y: -10,
              fill: 'red',
            },
          },
        children: [
            {
              name: "Yes! I would like to hear more Pros.",
              attributes: {
                
              },
              nodeSvgShape: {
                shape: 'rect',
                shapeProps: {
                  width: 20,
                  height: 20,
                  x: -10,
                  y: -10,
                  fill: 'red',
                },
              },
            },
          ],
      },
      {
        name: "No. Show me the cons now.",
      },
    ],
  },
];

export default class DTree extends React.Component {
  render() {
    return (
      // {/* <Tree /> will fill width/height of its container; in this case `#treeWrapper` */}

      <div id="treeWrapper" style={{ width: "50em", height: "20em" }}>
        <Tree data={myTreeData} />
      </div>
    );
  }
}
