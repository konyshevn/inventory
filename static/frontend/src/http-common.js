import axios from 'axios';

export const HTTP = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  // baseURL: 'http://localhost:8000/api/',
  // baseURL: 'http://www.inventory.na4u.ru/api',
  
  headers: {

  }
})