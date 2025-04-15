import React, { useState, useMemo } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import BuildingPopup from "./BuildingPopup";
import * as THREE from "three";

// Utility to compute the center of all lat/lng
function getOffset(buildings) {
  const lngs = [];
  const lats = [];

  buildings.forEach((b) => {
    b.coordinates.forEach(([lng, lat]) => {
      lngs.push(lng);
      lats.push(lat);
    });
  });

  const avgLng = lngs.reduce((a, b) => a + b, 0) / lngs.length;
  const avgLat = lats.reduce((a, b) => a + b, 0) / lats.length;

  return { lng: avgLng, lat: avgLat };
}

function Building({ building, onClick, isSelected, isHighlighted, offset, scale = 100000 }) {
  const shape = new THREE.Shape();

  if (!building.coordinates || building.coordinates.length < 3) {
    console.warn("Skipping building with invalid coordinates:", building);
    return null;
  }

  building.coordinates.forEach(([lng, lat], i) => {
    const x = (lng - offset.lng) * scale;
    const y = (lat - offset.lat) * scale;
    if (i === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  });

  const extrudeSettings = {
    depth: building.height || 10,
    bevelEnabled: false,
  };

  const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
  const roofGeometry = new THREE.ShapeGeometry(shape);
  const color = ((isSelected || isHighlighted) ? "orange" : "skyblue");

  return (
    <group
      rotation={[-Math.PI / 2, 0, 0]}
      onClick={(e) => {
        e.stopPropagation();
        onClick(building);
      }}
    >
      {/* Walls */}
      <mesh geometry={geometry}>
        <meshStandardMaterial color={color} />
      </mesh>

      {/* Roof */}
      <mesh geometry={roofGeometry} position={[0, 0, building.height]}>
        <meshStandardMaterial color={color} />
      </mesh>
    </group>
  );
}

export default function BuildingScene({ buildings, fetchedBuildings }) {
  const [selected, setSelected] = useState(null);

  // Compute offset once
  const offset = useMemo(() => getOffset(buildings), [buildings]);

  const highlightedIds = useMemo(() => new Set(fetchedBuildings.map(b => b.struct_id)), [fetchedBuildings]);

  return (
    <>
      <Canvas
        camera={{ position: [500, 500, 300], fov: 50, near: 1, far: 10000}}
      >
        <ambientLight intensity={0.6} />
        <pointLight position={[100, 100, 100]} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <OrbitControls minDistance={100} maxDistance={2000} />

        {/* Ground plane */}
        <mesh position={[0, 0, -2]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[2000, 2000]} />
          <meshStandardMaterial color="lightgreen" />
        </mesh>

        {/* Add the buildings */}
        {buildings.map((building, i) => (
          <Building
            key={i}
            building={building}
            offset={offset}
            onClick={setSelected}
            isSelected={selected?.struct_id === building.struct_id}
            isHighlighted={highlightedIds.has(building.struct_id)}
          />
        ))}
      </Canvas>

      {selected && (
        <BuildingPopup building={selected} onClose={() => setSelected(null)} />
      )}
    </>
  );
}
