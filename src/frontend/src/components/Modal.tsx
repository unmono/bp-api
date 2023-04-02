import { useContext } from 'react';
import { Link } from 'react-router-dom';

import {ModalContext, SubsectionModalContext} from "../App";

export default function Modal() {
  const closeModal = useContext(SubsectionModalContext);
  const productList = useContext(ModalContext);

  const products = productList && productList.length > 0
    ? productList.map(pr => {
      return (
        <li key={pr.part_no}>
          <Link
            to={`/products/${pr.part_no}`}
            onClick={closeModal && closeModal()}
          >
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