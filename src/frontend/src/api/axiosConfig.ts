import axios, { AxiosResponse } from 'axios';
import {json} from 'react-router-dom';

export const api = axios.create({
  baseURL:'http://localhost:8000',
});

export const bpGet = async (endpoint: string) => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.get(endpoint);
  } catch(error: any) {
    if(error.response) {
      throw json({
        code: error.response.status,
        message: error.response.data.detail,
      });
    }
  }

  return resp?.data;
}

export const searchPost = async (data: { search_query: string },
                                 endpoint: string = '/search/') => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.post(endpoint, data);
  } catch(error) {
    console.log(error);
  }

  return resp?.data;
}