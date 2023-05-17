import { useLoaderData } from 'react-router-dom';

import {SectionType} from "./Section";
import SubSection from "./SubSection";
import Section from "./Section";

export default function () {
  const sections = useLoaderData() as [SectionType];

  // const sectionBlocks = sections
  //   ? sections.map(renderSub)
  //   : undefined;

  const sectionsList = sections
    ? sections.map(s => <Section section={s} />)
    : undefined

  return (
    <ul className={'sections'}>
      {sectionsList}
    </ul>
  );
}