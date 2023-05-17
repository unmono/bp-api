import {useState, useEffect} from 'react';

import {bpGet} from "../api/axiosConfig";
import {ProductShortType, ProductLink} from "./ProductLink";

export default function ProductList(props: {endpoint: string}) {
  const [products, setProducts] = useState<[ProductShortType] | null>(null);

  useEffect(() => {
    bpGet(props.endpoint)
      .then(response => {
        setProducts(response);
      })
  }, [])

  const renderedProducts = products?.map(p => <ProductLink {...p} />)

  return (
    <ul>
      {products ? renderedProducts : '...'}
    </ul>
  )
}