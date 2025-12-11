import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000',  // Change this to your backend API URL
});

export const loginUser = async (username, password) => {
  return API.post('/login', { username, password });
};

export const registerUser = async (userData) => {
  return API.post('/register', userData);
};

export const fetchUtilities = async () => {
  return API.get('/utilities');
};

export const fetchBills = async () => {
  return API.get('/bills');
};

export const fetchReminders = async () => {
  return API.get('/reminders');
};
