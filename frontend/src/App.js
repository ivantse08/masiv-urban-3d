import React, { useEffect, useState } from "react";
import BuildingScene from "./components/BuildingScene";

function App() {
  const [buildings, setBuildings] = useState([]);
  const [fetchedBuildings, setFetchedBuildings] = useState([]);
  const [query, setQuery] = useState("");

  // Pull building data on start
  useEffect(() => {
    fetch("https://masiv-urban-3d.onrender.com/api/buildings")
      .then((res) => res.json())
      .then((data) => {
        setBuildings(data);
        setFetchedBuildings(data);
      });
  }, []);

  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    setLoading(true);
    try {
      const res = await fetch("https://masiv-urban-3d.onrender.com/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });
  
      const data = await res.json();
      setFetchedBuildings(data);
    } catch (err) {
      console.error("Query failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <div style={{ position: "absolute", top: 10, left: 10, zIndex: 10 }}>
        <input
          type="text"
          placeholder="Ask something like 'show tall buildings'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ padding: "8px", width: "300px", fontSize: "14px" }}
        />
        <button onClick={handleQuery} style={{ padding: "8px", marginLeft: "5px" }}>
          Submit
        </button>
        {loading && <p style={{ position: 'absolute', top: 50, left: 10 }}>Loading...</p>}
      </div>
      <BuildingScene buildings={buildings} fetchedBuildings={fetchedBuildings} />
    </div>
  );
}

export default App;