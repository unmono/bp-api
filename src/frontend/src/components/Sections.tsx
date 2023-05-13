import { useState, useEffect, useContext } from 'react';
import { useLoaderData } from 'react-router-dom';

import {SectionType} from "../types";
import SubSection from "./SubSection";
import PartnumPlaceholder from "./PartnumPlaceholder";
import {bpGet} from "../api/axiosConfig";
import {LoginContext} from "../contexts";

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