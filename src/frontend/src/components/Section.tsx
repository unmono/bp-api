import {useState} from 'react';

import ProductList from "./ProductList";
import PlusMinus from "./PlusMinus";

export interface SectionType {
  title: string;
  subsections?: [any];
  path?: string;
}

export default function Section (props: {section: SectionType}) {
  const [opened, setOpened] = useState<boolean>(false);
  const s = props.section;

  const renderSub = () => {
    if(s.subsections) {
      const subsections = s.subsections.map(
        sub => <Section section={sub}/>
      )
      return <ul>{subsections}</ul>;
    } else if(s.path) {
      return <ProductList endpoint={s.path} />
    }
  }

  const openSection = () => {
    setOpened(!opened);
  }

  return(
    <li key={s.title}>
      <div onClick={openSection}>
        <PlusMinus sw={opened} />
        {s.title}
      </div>
      {opened && renderSub()}
    </li>
  )
}