// ChatBox.jsx
import React from "react";
import "react-chatbox-component/dist/style.css";
import { ChatBox } from "react-chatbox-component";

const messages = [
  {
    text: "Hello there",
    id: "1",
    sender: {
      name: "Ironman",
      uid: "user1",
      },
  },
];
const user = {
  uid: "user1",
};

export default class App extends React.Component {
  render() {
    return (
      <div className="container">
        <div className="chat-header">
          <h5>Chat History</h5>
        </div>
        <ChatBox messages={messages} user={user} />
      </div>
    );
  }
}
