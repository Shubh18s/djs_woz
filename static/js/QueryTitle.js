import React, { useState, useEffect } from "react";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

export default class QueryTitle extends React.Component {
  render() {
    return (
      <div>
        <Card>
          <Card.Body>
            <div id="place_for_query">
              <Card.Title></Card.Title>
            </div>
            <Card.Text>
            <h3>The current query is Hello.</h3>
            </Card.Text>
            <Button variant="primary">Go somewhere</Button>
          </Card.Body>
        </Card>
      </div>
    );
  }
}
