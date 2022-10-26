import React from "react";

import { Button, Row, Col, Card, Nav } from "react-bootstrap";
import Sampletxt from "components/UI/Sampletxt";

const _thrid_row = () => {
  return (
    <Row id="3th-row">
      <Col
        style={{
          marginTop: "15px",
        }}
      >
        <Card>
          <Card.Header
            style={{
              fontSize: "1.4rem",
              fontWeight: "600",
              textAlign: "center",
            }}
          >
            Graphical Status
          </Card.Header>
          <Card.Header>
            <Nav variant="pills" defaultActiveKey="#first">
              <Nav.Item>
                <Nav.Link href="#first">Detection Data</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#second">Axis Data</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#third">Running Time</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link href="#fourth">Manipulator Status</Nav.Link>
              </Nav.Item>
            </Nav>
          </Card.Header>
          <Card.Body>
            <Card.Title>Graphical Data</Card.Title>
            <Card.Text as="div">
              <Sampletxt></Sampletxt>
            </Card.Text>
            <Button variant="success">OK</Button>
          </Card.Body>
          <Card.Footer>updated : latest</Card.Footer>
        </Card>
      </Col>
    </Row>
  );
};

export default _thrid_row;
