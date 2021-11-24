import axios from "axios";
import QueryString from "qs";
import { handleError, isOk } from './functions';
import store from "./store";

axios.defaults.baseURL = 'https://naass.nginxplus.co.kr/api';
axios.defaults.withCredentials = true;
axios.defaults.headers['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers['Access-Control-Allow-Headers'] = '*';

axios.interceptors.response.use(res => {
    store.dispatch('unsetError');
    return res;
}, error => Promise.reject(handleError(error)));

const formsHeader = { headers: { 'Content-Type': 'application/x-www-form-urlencoded', ...axios.defaults.headers }, ...axios.defaults };

export const login = (email, password) => axios.post('/token', QueryString.stringify({ username: email, password }), formsHeader).catch(handleError);

export const logout = () => axios.delete('/token').then(res => isOk(res.status)).catch(handleError);

export const createUser = (email, password) => axios.post('/users', QueryString.stringify({ username: email, password }), formsHeader);

export const getMyInfo = () => axios.get('/users/me').catch(handleError);

export const sendPasswordResetEmail = email => axios.post('/forgot-password', { email }).then(res => isOk(res.status)).catch(handleError);

export const resetPassword = (token, password) => axios.post('/reset-password', { token, password }).then(res => isOk(res.status)).catch(handleError);

export const getProfiles = () => axios.get('/profiles').catch(handleError);

export const createProfile = (userId, profile) => axios.post(`/users/${userId}/profiles`, profile).catch(handleError);

export const deleteProfile = id => axios.delete(`/profiles/${id}`).then(res => isOk(res.status)).catch(handleError);

export const editProfile = (id, profile) => axios.put(`/profiles/${id}`, profile).then(res => isOk(res.status)).catch(handleError);