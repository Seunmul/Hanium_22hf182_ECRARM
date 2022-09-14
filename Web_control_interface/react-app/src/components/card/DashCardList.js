import React from "react";
import DashCard from "./DashCard";

const dashCount = [1, 2, 3, 4, 5, 6];
const DashCards = dashCount.map((v, i) => {
  return <DashCard key={i} num={v} />;
});

const DashCardList = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        flexWrap: "wrap",
        justifyContent: "space-evenly",
        alignContent: "center",
        
      }}
    >
      {DashCards}
    </div>
  );
};

export default DashCardList;
