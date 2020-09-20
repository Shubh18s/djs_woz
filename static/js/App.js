// App.jsx
import React from "react";
import Tree from 'react-tree-graph';
import 'react-tree-graph/dist/style.css'
export default class App extends React.Component {
    data = {
        name:'Parent',
        children:[{
            name:'Child One'
        }, {
            name:'Child Two'
        }]
    };
  render () {
    return (<div>
         <Tree data={data}
    height={800}
    width={800}/>
    </div>);
    
  }
}