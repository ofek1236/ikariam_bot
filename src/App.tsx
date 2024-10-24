import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Action from "./components/Action.tsx";

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Action buildingName={"Academy"} newLevel={6} timeToBuild={"123"} endTime={"1234"}></Action>
    </>
  )
}

export default App
