import axios from "axios";
import { handleError } from './functions';

axios.defaults.baseURL = 'http://localhost:8000/api';

const formsHeader = { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } };

export const login = (username, password) => axios.post('/login', { username, password }, formsHeader).catch(handleError);

export const logout = () => axios.post('/logout').then(res => res.status == 200).catch(handleError);

export const createUser = (username, email, password) => axios.post('/users/create', { username, email, password }, formsHeader).catch(handleError);

export const getProfiles = () => axios.get('/profiles').catch(handleError);

export const getProfile = (id) => axios.get(`/profiles/${id}`).catch(handleError);

export const editProfile = (id) => axios.post(`/profiles/${id}/edit`).then(res => res.status == 200).catch(handleError);