// src/components/Login.tsx

import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { RegisterDialog } from "./register";
import { UserContext, axiosInstance } from "@/lib/utils";


const Login: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const { setData } = useContext(UserContext);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // Simulate a login process
        const data = { "email": email, "password": password }
        axiosInstance.post("/login", data)
            .then((response) => {
                let data = response.data;
                if (data.success === true) {
                    // Handle login logic here
                    setData({
                        "user": "TEST",
                        "id": response.data.user_id
                    })
                    setError(''); // Clear error if login is successful
                    navigate(`/projects/${data.user_id}`); // Change '/dashboard' to your desired route
                } else {
                    setError(data.error);
                }
            })
    };

    return (
        <div className="flex w-screen items-center justify-center min-h-screen bg-gray-100">
            <form
                onSubmit={handleSubmit}
                className="bg-white p-6 rounded-lg shadow-md w-96"
            >
                <h2 className="text-2xl font-bold text-center mb-6">Login</h2>

                {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

                <div className="mb-4">
                    <label htmlFor="email" className="block text-gray-700 mb-2">
                        Email
                    </label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                </div>

                <div className="mb-6">
                    <label htmlFor="password" className="block text-gray-700 mb-2">
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="w-full p-2 border border-gray-300 rounded"
                    />
                </div>
                <div className='flex flex-col-1 p-2'>
                    <button
                        type="submit"
                        className="w-full bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                    >
                        Login
                    </button>
                    <RegisterDialog />
                </div>
            </form>
        </div>
    );
};

export default Login;
