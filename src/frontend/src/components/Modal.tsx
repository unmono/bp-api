import { useContext } from 'react';
import { Link } from 'react-router-dom';

import { ProductShortType } from "../types";
import {SubsectionModalContext} from "../App";

export default function (props: {productList: [ProductShortType]}) {
  const closeModal = useContext(SubsectionModalContext)

  const products = props.productList && props.productList.length > 0
    ? props.productList.map(pr => {
      return (
        <li key={pr.part_no}>
          <Link to={`/products/${pr.part_no}`} onClick={closeModal && closeModal()}>
            {`${pr.part_no} - ${pr.title_en}`}
          </Link>
        </li>
      )
    })
    : <p>Nothing =(</p>

  return (
    <div className={'product-list-modal'}>
      <div className={'modal-content'}>
        <div className={'modal-top'}>
          <span onClick={closeModal && closeModal()}>&times;</span>
        </div>
        <div className={'product-list'}>
          <ul>{products}</ul>
        </div>
      </div>
    </div>
  );
}