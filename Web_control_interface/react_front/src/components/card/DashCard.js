import React from "react";
import { Card } from "react-bootstrap";

const DashCard = (props) => {
  return (
    <Card
      style={{
        height: "23rem",
        minWidth: "300px",
        width:"30%",
        maxWidth: "800px",
        margin: "1rem 0rem",
      }}
    >
      <Card.Header as="h5">No.{props.num}</Card.Header>
      <Card.Body>
        <Card.Title>Title</Card.Title>
        <Card.Subtitle className="mb-2 text-muted">Card Subtitle</Card.Subtitle>
        <Card.Text>
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </Card.Text>
        <Card.Link href="#">Card Link</Card.Link>
        <Card.Link href="#">Another Link</Card.Link>
      </Card.Body>
    </Card>
  );
};

export default DashCard;
