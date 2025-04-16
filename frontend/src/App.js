import React, { useEffect, useState } from "react";
import BuildingScene from "./components/BuildingScene";

function App() {
  const [buildings, setBuildings] = useState([]);
  const [fetchedBuildings, setFetchedBuildings] = useState([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Pull building data on start
  useEffect(() => {
    fetch("https://masiv-urban-3d.onrender.com/api/buildings")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      })
      .then((data) => {
        setBuildings(data);
      })
      .catch((error) => {
        console.error("Error fetching buildings:", error);
      });
  }, []);

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
      setError("There was an issue with your query. Please try tweaking your prompt.");
      setFetchedBuildings([]);
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
        {error && <p style={{ position: 'absolute', top: 50, left: 10, color: 'red' }}>{error}</p>}
      </div>
      <BuildingScene buildings={buildings} fetchedBuildings={fetchedBuildings} />
    </div>
  );
}

export default App;