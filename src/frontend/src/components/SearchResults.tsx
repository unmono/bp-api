import {useState, useEffect} from 'react';
import {useLocation, useNavigate} from 'react-router-dom';

import {ProductShortType, ProductLink} from './ProductLink';
import {searchPost} from "../api/axiosConfig";
import PlusMinus from "./PlusMinus";

export default function SearchResults() {
  const [products, setProducts] = useState<[ProductShortType] | null>(null);
  const {state} = useLocation();
  const {searchQuery} = state;
  const navigate = useNavigate();

  useEffect(() => {
    if(searchQuery) {
      searchPost({search_query: searchQuery}).then(response => {
        if(response.length === 1) {
          navigate(`/products/${response[0].part_no}`);
          return;
        }
        setProducts(response);
      });
    }
  }, [state]);

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