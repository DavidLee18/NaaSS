import axios from "axios";
import QueryString from "qs";
import { handleError } from './functions';

axios.defaults.baseURL = 'https://naass.nginxplus.co.kr/api';
axios.defaults.withCredentials = true;
axios.defaults.headers['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers['Access-Control-Allow-Headers'] = '*';

const formsHeader = { headers: { 'Content-Type': 'application/x-www-form-urlencoded', ...axios.defaults.headers }, ...axios.defaults };

export const login = (email, password) => axios.post('/token', QueryString.stringify({ username: email, password }), formsHeader).catch(handleError);

export const logout = () => axios.delete('/token').then(res => res.status == 200).catch(handleError);

export const createUser = (email, password) => axios.post('/users', QueryString.stringify({ username: email, password }), formsHeader);

export const getMyInfo = () => axios.get('/users/me').catch(handleError);

export const getProfiles = () => axios.get('/profiles').catch(handleError);

export const createProfile = (userId, profile) => axios.post(`/users/${userId}/profiles`, profile).catch(handleError);

export const deleteProfile = id => axios.delete(`/profiles/${id}`).then(res => res.status === 200).catch(handleError);

export const editProfile = (id, profile) => axios.put(`/profiles/${id}`, profile).then(res => res.status === 200).catch(handleError);