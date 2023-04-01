import React, { useContext } from 'react';

import {SubSectionType} from "../types";
import {SubsectionModalContext} from "../App";

export default function (props: SubSectionType) {
  const listSubsectionInModal = useContext(SubsectionModalContext);

  const subSectionLinks = props.subsections.map(s => {
    return <li key={s.url}>
      <a onClick={ listSubsectionInModal &&  listSubsectionInModal(s.url) }>{s.title}</a>
    </li>
  });

  return (
    <li key={props.title}>
      <div>{props.title}</div>
      <ul>
        {subSectionLinks}
      </ul>
    </li>
  );
}