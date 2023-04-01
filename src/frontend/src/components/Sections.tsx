import { useState, useEffect } from 'react';

import { api, bpGet } from "../api/axiosConfig";
import {SectionType} from "../types";
import SubSection from "./SubSection";

export default function () {
  const [sections, setSections] = useState<[SectionType]>();

    useEffect(() => {
      bpGet('/sections').then(sections => {
        setSections(sections?.data);
      })
    }, []);

    const renderSub = (s: SectionType) => {
      const subsections = s.subsections.map(
        sub => <SubSection {...sub} />
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
        <div className={'partnum-placeholder'}>
          Search for product,<br />
          or select from sections.
        </div>
        <ul className={'sections'}>
          {sectionBlocks}
        </ul>
      </>
    );
}