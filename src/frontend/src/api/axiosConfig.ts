import axios, { AxiosResponse } from 'axios';
import {json, useNavigate} from 'react-router-dom';

export const api = axios.create({
  baseURL:'http://localhost:8000/api/v1',
});

export const bpGet = async (
  endpoint: string,
  accessToken: string
) => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.get(
      endpoint,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
  } catch(error: any) {
    if(error.response) {
      // if(error.response.status == 401) {
      //
      // }
      throw json({
        code: error.response.status,
        message: error.response.data.detail,
      });
    }
  }

  return resp?.data;
}

export const searchPost = async (
  data: { search_query: string },
  accessToken: string,
  endpoint: string = '/products/search/'
) => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.post(
      endpoint,
      data,
      {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
  } catch(error) {
    console.log(error);
  }

  return resp?.data;
}

export const login = async (username: string, password: string) => {
  const credentials = {
    username: username,
    password: password,
  }
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.post(
      '/login/',
      credentials,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    );
  } catch(error) {
    console.log(error);
  }

  return resp?.data.access_token
}