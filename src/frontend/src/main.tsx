import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  createRoutesFromElements,
  json,
  Route,
  RouterProvider
} from 'react-router-dom';

import App from './App';
import './index.css';
import {bpGet} from "./api/axiosConfig";
import Sections from "./components/Sections";
import {validatePartnum} from "./functions";
import ProductInfo from "./components/ProductInfo";
import ErrorComponent from "./components/ErrorComponent";
import LoginForm from "./components/LoginForm";

const routes = (
  <Route
    path={'/'}
    element={<App />}
  >
    <Route
      index
      loader={
        async _ => await bpGet('/sections')
      }
      element={<Sections />}
      errorElement={<ErrorComponent />}
    />
    <Route
      path={'/products/:partNum'}
      loader={
        async ({params}) => {
          if(params.partNum && validatePartnum(params.partNum)) {
            return await bpGet(`/products/${params.partNum}`)
          } else {
            throw json({
              code: 404,
              message: 'No such product, bitch.'
            });
          }
        }
      }
      element={<ProductInfo />}
      errorElement={<ErrorComponent />}
    />
    <Route
      path={'login'}
      element={<LoginForm />}
    />
  </Route>
);

const router = createBrowserRouter(createRoutesFromElements(routes));

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
