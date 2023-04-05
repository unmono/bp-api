import React, { useContext } from 'react';

import {SubSectionType} from "../types";
import {SubsectionModalContext} from "../contexts";

export default function (props: SubSectionType) {
  const listSubsectionInModal = useContext(SubsectionModalContext);

  const subSectionLinks = props.subsections.map(s => {
    return <li key={`subsub${s.path}`}>
      <a onClick={ listSubsectionInModal && listSubsectionInModal(s.path) }>{s.title}</a>
    </li>
  });

  return (
    <li>
      <div>{props.title}</div>
      <ul>
        {subSectionLinks}
      </ul>
    </li>
  );
}