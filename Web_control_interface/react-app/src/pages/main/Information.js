import React from "react";

const Information = ({ style }) => {
  return (
    <div style={style}>
      <div>
        <h4>Program Title : {process.env.REACT_APP_SERVICE_TITLE}</h4>
        <h4>Program Version : {process.env.REACT_APP_SERVICE_VERSION}</h4>
      </div>
    </div>
  );
};

export default Information;
