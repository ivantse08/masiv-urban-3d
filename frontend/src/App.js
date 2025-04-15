import React, { useEffect, useState } from "react";
import BuildingScene from "./components/BuildingScene";

function App() {
  const [buildings, setBuildings] = useState([]);

  useEffect(() => {
    fetch("https://masiv-urban-3d.onrender.com/api/buildings")
      .then((res) => res.json())
      .then((data) => {
        setBuildings(data);
        // console.log("Fetched buildings:", JSON.stringify(data, null, 2));
      });
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      Text to see it works
      <BuildingScene buildings={buildings} />
    </div>
  );
}

export default App;