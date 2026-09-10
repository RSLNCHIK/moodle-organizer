import { useEffect, useRef, useState } from "react";

function InteractiveGridBackground() {
  const [tiles, setTiles] = useState([]);
  const lastTile = useRef(null);

  useEffect(() => {
    const size = 96;

    function handleMouseMove(event) {
      const x = Math.floor(event.clientX / size) * size;
      const y = Math.floor(event.clientY / size) * size;

      const position = `${x}-${y}`;

      // Solange die Maus im gleichen Kästchen bleibt,
      // kein neues Quadrat erzeugen
      if (lastTile.current === position) {
        return;
      }

      lastTile.current = position;

      const id = `${position}-${Date.now()}`;

      setTiles((previousTiles) => [
        ...previousTiles.slice(-5),
        {
          id,
          x,
          y,
        },
      ]);

      setTimeout(() => {
        setTiles((previousTiles) =>
          previousTiles.filter((tile) => tile.id !== id)
        );
      }, 1800);
    }

    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">

      {/* Hintergrund-Grid */}
      <div
        className="
          absolute inset-0
          bg-[linear-gradient(to_right,#e8eaf2_1px,transparent_1px),linear-gradient(to_bottom,#e8eaf2_1px,transparent_1px)]
          bg-[size:96px_96px]
          opacity-35
        "
      />

      {/* Mausspur */}
      {tiles.map((tile) => (
        <div
          key={tile.id}
          className="
            absolute h-24 w-24
            bg-violet-300/20
            animate-[tileFade_1.8s_ease-out_forwards]
          "
          style={{
            left: tile.x,
            top: tile.y,
          }}
        />
      ))}
    </div>
  );
}

export default InteractiveGridBackground;