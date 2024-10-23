import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import axios from 'axios';
import React, { createContext } from "react";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const axiosInstance = axios.create({
  baseURL: 'http://localhost:5000',
});


export interface UserData {
  user: string,
  id: string
}

export interface UserContextData {
  user_data: UserData,
  setData: React.Dispatch<React.SetStateAction<UserData>>
}

export const UserContext = createContext<UserContextData>(null);