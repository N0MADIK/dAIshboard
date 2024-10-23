
import './App.css'
import NavBar from './components/navigator'
import { Routes, Route } from 'react-router-dom';
import { lazy, Suspense, useState } from 'react';
import { UserContext, UserContextData, UserData } from './lib/utils.ts';

const Login = lazy(() => import('./components/login/index.tsx'));
const Projects = lazy(() => import('./components/projects/index.tsx'));
const Canvas = lazy(() => import('./components/canvas/index.tsx'));




function App() {
  const [userData, setUserData] = useState<UserData>({});

  return (
    <UserContext.Provider value={{ user_data: userData, setData: setUserData }}>
      <div className='flex w-screen'>
        <Suspense fallback={<div className="container">Loading...</div>}>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/login" element={<Login />} />
            <Route path="/projects/:user_id" element={<Projects />} />
            <Route path="/canvas/:user_id/:project_id" element={<Canvas />} />
          </Routes>
        </Suspense>
      </div>
    </UserContext.Provider>
  )
}

export default App
