import { useState, useEffect, useContext } from 'react';
import { useParams, Link, useLoaderData, json } from 'react-router-dom';

import {
  MasterDataType,
  PartType,
  ProductShortType,
  ProductType
} from "../types";
import {SubsectionModalContext} from '../contexts';

export default function ProductInfo () {
  const part = useLoaderData() as PartType;

  const boschThisNumber = (v: string) =>
    `${v.slice(0, 1)} ${v.slice(1, 4)} ${v.slice(4, 7)} ${v.slice(7, 10)}`;

  return (
    <>
      <div className={'part-number-block'}>
        <div className={'part-number'}>
          { part?.part_no && boschThisNumber(part.part_no) }
        </div>
        <div className={'new-release'}>
          { part?.new_release && '* New release'}
        </div>
        <div className={'discontinued'}>
          { part?.discontinued && '* Discontinued'}
        </div>
      </div>
      <div className={'product-info'}>
        <div className={'product-info-general'}>
          <div>
            { part?.product && <GeneralInfo {...part.product} /> }
          </div>
          <div>
            { part?.masterdata && <MasterData {...part.masterdata} /> }
          </div>
        </div>
        <div className={'refers'}>
          { part?.refers && <Refers refersList={part.refers} /> }
        </div>
      </div>
    </>
  );
}

const GeneralInfo = (props: ProductType) => {
  const listGroupInModal = useContext(SubsectionModalContext);

  return(
    <table className={'product-info-table'}>
      <thead>
        <tr>
          <th colSpan={2}>Product info</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Title UA</td>
          <td>{props.title_ua}</td>
        </tr>
        <tr>
          <td>Title EN</td>
          <td>{props.title_en}</td>
        </tr>
        <tr>
          <td>UKTZED</td>
          <td>{props.uktzed}</td>
        </tr>
        <tr>
          <td>Minimal order</td>
          <td>{props.min_order}</td>
        </tr>
        <tr>
          <td>Qantity in product</td>
          <td>{props.quantity}</td>
        </tr>
        <tr>
          <td>Retail price</td>
          <td>{props.price}</td>
        </tr>
        <tr>
          <td>Truck stock</td>
          <td>{props.truck ? 'yes' : 'no'}</td>
        </tr>
        <tr>
          <td>Section</td>
          <td>
            <a href={'#'} onClick={listGroupInModal && listGroupInModal(props.group.path)}>{props.group.title}</a>
          </td>
        </tr>
      </tbody>
    </table>
  );
}

const MasterData = (props: MasterDataType) => {
  return (
    <table className={'product-info-table'}>
      <thead>
        <tr>
          <th colSpan={2}>Masterdata</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>EAN</td>
          <td>{props.ean}</td>
        </tr>
        <tr>
          <td>Gross weight</td>
          <td>{`${props.gross} ${props.weight_unit}`}</td>
        </tr>
        <tr>
          <td>Net weight</td>
          <td>{`${props.net} ${props.weight_unit}`}</td>
        </tr>
        <tr>
          <td>Dimensions L x W x H</td>
          <td>{`${props.length} x ${props.width} x ${props.height} ${props.measure_unit}`}</td>
        </tr>
        <tr>
          <td>Volume</td>
          <td>{`${props.volume} ${props.volume_unit}`}</td>
        </tr>
      </tbody>
    </table>
  );
}

const Refers = (props: { refersList: [ProductShortType] }) => {
  const refersItems = props.refersList.length
    ? props.refersList.map( ref => {
      return (
        <li key={ref.part_no}>
          <Link to={`/products/${ref.part_no}`}>{ref.part_no}</Link>
        </li>
      )
    })
    : <li className={'noRefers'}>No refers</li>

  return (
    <>
      <div>Refers</div>
      <ul>
        {refersItems}
      </ul>
    </>
  );
}