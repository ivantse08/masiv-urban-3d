import React from "react";

export default function BuildingPopup({ building, onClose }) {
  return (
    <div style={{
      position: "absolute",
      top: 20,
      right: 20,
      background: "white",
      border: "1px solid #ccc",
      padding: 10,
      borderRadius: 8,
      zIndex: 1000
    }}>
      <h3>Building Info</h3>
      <p><b>Struct ID:</b> {building.struct_id}</p>
      <p><b>Height:</b> {building.height} m</p>
      <p><b>Stage:</b> {building.stage}</p>
      <button onClick={onClose}>Close</button>
    </div>
  );
}
