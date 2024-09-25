
import './App.css'
import NavBar from './components/navigator'
import { Routes, Route } from 'react-router-dom';
import { lazy, Suspense } from 'react';

const Login = lazy(() => import('./components/login/index.tsx'));
const Projects = lazy(() => import('./components/projects/index.tsx'));
const Canvas = lazy(() => import('./components/canvas/index.tsx'));

function App() {

  return (
    <div className='flex w-screen'>
      <Suspense fallback={<div className="container">Loading...</div>}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/canvas" element={<Canvas />} />
        </Routes>
      </Suspense>
    </div>
  )
}

export default App
