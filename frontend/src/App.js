import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Canvas from "./Canvas";
import { Input, Switch } from "@mui/material";

const initialRectangles = [
  {
    id: "tachometer",
    name: "Tacometro",
    x: 0,
    y: 0,
    scale: 1,
    img: "/tachometer-bg.png",
  },
  {
    id: "speedometer",
    name: "Velocimetro",
    x: 0,
    y: 0,
    scale: 1,
    img: "/speedometer-bg.png",
  },
  {
    id: "twostep",
    name: "Two Step",
    x: 0,
    y: 0,
    scale: 1,
    img: "/2step.png",
  },
  {
    id: "lambda",
    name: "Sonda Lambda",
    x: 0,
    y: 0,
    scale: 1,
    img: "/overlay-wideband.png",
  },
];

function App() {
  const [rectangles, setRectangles] = useState(initialRectangles);
  const [log, setLog] = useState(null);

  function readFile(input) {
    let file = input.target.files[0];

    let reader = new FileReader();

    reader.readAsText(file);

    reader.onload = function () {
      console.log(reader.result);
      setLog(reader.result);
    };

    reader.onerror = function () {
      console.log(reader.error);
    };
  }

  return (
    <div className="App">
      <header className="App-header">
        {rectangles.map((r, i) => (
          <>
            <Switch
              onChange={(_, checked) =>
                setRectangles((prev) => {
                  prev[i].enabled = checked;
                  return [...prev];
                })
              }
            />
            {r.name}
          </>
        ))}
        <Input type="file" onChange={readFile} />
        <Canvas
          log={log}
          rectangles={rectangles}
          setRectangles={setRectangles}
        />
        {/* <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
      </header>
    </div>
  );
}

export default App;
