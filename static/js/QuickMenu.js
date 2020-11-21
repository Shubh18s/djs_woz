import React, { useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import { Container, Row, Col, ButtonGroup } from "reactstrap";
// import ButtonGroup from 'react-bootstrap/ButtonGroup'

export default class QuickMenu extends React.Component {
  sendPreviousResponse() {
    alert("Sending Previous Response");
  }

  requestPreviousResponse() {
    alert("I'm Sorry. Could you please repeat that?");
  }

  render() {
    return (
      <div>
        <ButtonGroup>
              <Button variant="primary" onClick={this.sendPreviousResponse}>
                Repeat Response
              </Button>
              &nbsp;&nbsp;
              <Button variant="primary" onClick={this.requestPreviousResponse}>
                Request User Utterance
              </Button>
              </ButtonGroup>
      </div>
    );
  }
}
