import {useLoaderData} from 'react-router-dom';
import {MasterDataType, ProductShortType, ProductType} from "../types";
import PartNumber from "./PartNumber";
import {PartPriceData, PriceDataType} from "./PartPriceData";
import Refers from "./Refers";

export interface PartType {
  part_no: string;
  discontinued: boolean;
  new_release: boolean;
  product?: PriceDataType;
  masterdata?: MasterDataType;
  refers: [ProductShortType];
}

export default function Part() {
  const part = useLoaderData() as PartType;

  return (
    <div className={'content'}>
      <div className={'part-block'}>
        <div>
          <PartNumber
            part_no={part.part_no}
            new_release={part.new_release}
            discontinued={part.discontinued}
          />
          {part.product && <PartPriceData blockName={'Pricelist data'} data={part.product} />}
          {part.masterdata && <PartPriceData blockName={'Master data'} data={part.masterdata} />}
        </div>
        {part.refers && <Refers refersList={part.refers} />}
      </div>
    </div>
  );
}