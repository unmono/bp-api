import {Link} from 'react-router-dom';

export interface ProductShortType {
  part_no: string;
  title_en: string;
  path: string;
}

export function ProductLink(props: ProductShortType) {
  return (
    <li key={props.part_no}>
      <Link to={props.path} className={'simple-link'}>
        {props.part_no}
        {props.title_en && ` - ${props.title_en}`}
      </Link>
    </li>
  )
}