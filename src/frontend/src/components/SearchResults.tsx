import {useState, useEffect} from 'react';
import {useLocation, useNavigate, json} from 'react-router-dom';
import {AxiosResponse} from 'axios';

import {ProductShortType, ProductLink} from './ProductLink';
import {searchPost} from "../api/axiosConfig";
import PlusMinus from "./PlusMinus";
import ErrorLayout from "./ErrorLayout";

type LittleErrorType = {
  status: number,
  data: {
    detail: string
  }
}

export default function SearchResults() {
  const [products, setProducts] = useState<[ProductShortType] | null>(null);
  const [errorResponse, setErrorResponse] = useState<AxiosResponse | LittleErrorType | null>(null);
  const {state} = useLocation();
  const {searchQuery} = state;
  const navigate = useNavigate();

  useEffect(() => {
    if(searchQuery) {
      searchPost({search_query: searchQuery})
        .then(response => {
          if(response.length === 1) {
            navigate(
              `/products/${response[0].part_no}`,
              {replace: true}
            );
            return;
          }
          setProducts(response);
        })
        .catch((error: any) => {
          if(error.response) {
            setErrorResponse(error.response);
          } else {
            setErrorResponse({
              status: 503,
              data: {
                detail: 'Server doesn\'t respond'
              }
            })
          }
        });
    }
  }, [state]);

  if(errorResponse) {
    return <ErrorLayout code={errorResponse.status} message={errorResponse.data.detail} />;
  }

  const productsList = products?.map(p => <ProductLink {...p} />);
  return (
    <div className={'search-results'}>
      <div className={'search-list-header'}>
      <PlusMinus sw={true} />
      {
        products && products.length > 0
          ? 'Search results'
          : 'Nothing'
      }
      </div>
      <ul>{productsList}</ul>
    </div>
  )
}