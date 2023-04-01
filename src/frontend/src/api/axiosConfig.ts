import axios, {AxiosResponse} from 'axios';

export const api = axios.create({
    baseURL:'http://localhost:8000',
});

export const bpGet = async (endpoint: string) => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.get(endpoint);
  } catch(error) {
    console.log(error);
  }

  return resp;
}

export const searchPost = async (data: { search_query: string },
                                 endpoint: string = '/search/') => {
  let resp: AxiosResponse<any, any> | null = null;
  try {
    resp = await api.post(endpoint, data);
  } catch(error) {
    console.log(error);
  }

  return resp;
}