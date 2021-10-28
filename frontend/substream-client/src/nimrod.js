import axios from "axios";
import { handleError } from './functions';

axios.defaults.baseURL = 'http://localhost:8000/api';

const formsHeader = { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } };

export const login = (email, password) => axios.post('/token', { username: email, password }, formsHeader).catch(handleError);

export const createUser = (email, password) => axios.post('/users', { username: email, password }, formsHeader).catch(handleError);

export const getMyInfo = () => axios.get('/users/me').catch(handleError);

export const getProfiles = () => axios.get('/profiles').catch(handleError);

export const deleteProfile = (id) => axios.delete(`/profiles/${id}`).catch(handleError);

export const editProfile = (id) => axios.put(`/profiles/${id}`).then(res => res.status == 200).catch(handleError);