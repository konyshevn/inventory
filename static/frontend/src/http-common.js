import axios from 'axios';

export const HTTP = axios.create({
  baseURL: 'http://localhost:8000/api/',
  // baseURL: 'http://www.inventory.na4u.ru/api',
  
  headers: {

  }
})