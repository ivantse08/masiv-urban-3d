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
      <p><b>Height:</b> {building.height}m</p>
      <p><b>Stage:</b> {building.stage}</p>
      {building.extra && (
        <>
            <p><b>Building Type:</b> {building.extra.building_type}</p>
            <p><b>Building Code:</b> {building.extra.building_type}</p>
            <p><b>Area:</b> {building.extra.area}m^2</p>
            <p><b>Perimeter:</b> {building.extra.perimeter}m</p>
            <p><b>Obscured:</b> {building.extra.obscured}</p>
        </>
        )}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
