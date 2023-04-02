import { useLoaderData } from 'react-router-dom';

import {SectionType} from "../types";
import SubSection from "./SubSection";
import PartnumPlaceholder from "./PartnumPlaceholder";

export default function () {
  const sections = useLoaderData() as [SectionType];

    const renderSub = (s: SectionType) => {
      const subsections = s.subsections.map(
        sub => <SubSection {...sub} key={`sub${sub.title}`} />
      );
      return (
        <li key={s.title}>
          <div>{ s.title }</div>
          <ul>{ subsections }</ul>
        </li>
      )
    }

    const sectionBlocks = sections
      ? sections.map(renderSub)
      : undefined;

    return (
      <>
        <PartnumPlaceholder />
        <ul className={'sections'}>
          {sectionBlocks}
        </ul>
      </>
    );
}