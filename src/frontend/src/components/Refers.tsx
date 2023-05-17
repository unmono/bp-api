import {Link} from 'react-router-dom';

import {ProductShortType, ProductLink} from "./ProductLink";

const Refers = (props: { refersList: [ProductShortType] }) => {
  const refersItems = props.refersList.map( ref => {
    return (
      <li key={ref.part_no}>
        <ProductLink {...ref} />
      </li>
    )
  })

  return (
    <div className={'refers-block'}>
      <div>{refersItems.length ? 'Refers to:' : 'No references'}</div>
      <ul>
        {refersItems}
      </ul>
    </div>
  );
}

export default Refers;