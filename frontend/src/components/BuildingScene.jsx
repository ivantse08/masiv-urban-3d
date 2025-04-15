import React, { useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import BuildingPopup from "./BuildingPopup";

function Building({ building, onClick, isSelected }) {
  const shape = new THREE.Shape();
  building.coordinates.forEach(([x, y], i) => {
    if (i === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  });

  const extrudeSettings = { depth: building.height || 10, bevelEnabled: false };
  const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
  const color = isSelected ? "orange" : "skyblue";

  return (
    <mesh
      geometry={geometry}
      onClick={(e) => {
        e.stopPropagation();
        onClick(building);
      }}
    >
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

export default function BuildingScene({ buildings }) {
  const [selected, setSelected] = useState(null);

  return (
    <>
      <Canvas camera={{ position: [0, 0, 100], fov: 50 }}>
        <ambientLight />
        <pointLight position={[100, 100, 100]} />
        <OrbitControls />

        {buildings.map((b, i) => (
          <Building
            key={i}
            building={b}
            onClick={setSelected}
            isSelected={selected?.struct_id === b.struct_id}
          />
        ))}
      </Canvas>
      {selected && <BuildingPopup building={selected} onClose={() => setSelected(null)} />}
    </>
  );
}
