import {SectionType} from "./Section";
import PlusMinus from "./PlusMinus";

export interface PriceDataType {
  title_ua: string;
  title_en: string;
  uktzed: number;
  min_order: number;
  quantity: number;
  price: number;
  truck: boolean;
  group: SectionType;
}

export const PartPriceData = (props: {blockName: string, data: Object}) => {
  const renderData = Object.entries(props.data).map(([key, value]) => {
    let output: string;
    switch(typeof value){
      case 'boolean':
        output = value ? 'Yes' : 'No';
        break;

      case 'object':
        if(!value) output = 'No data';
        else output = value.title;
        break;

      default:
        output = value;
    }
    let priceClass = '';
    if(key === 'price') {
      priceClass = 'price-color';
    }
    return (
      <li key={key} className={priceClass}>
        <div>{key.charAt(0).toUpperCase() + key.slice(1)}</div>
        <div>{output}</div>
      </li>
    )
  });

  return (
    <div className={'part-data'}>
      <div className={'part-data-header'}><PlusMinus sw={true} />{props.blockName}</div>
      <ul className={'part-data-list'}>
        {renderData}
      </ul>
    </div>
  );
}