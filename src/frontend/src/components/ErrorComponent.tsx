import { useRouteError } from 'react-router-dom';

import PartnumPlaceholder from "./PartnumPlaceholder";

export default function ErrorComponent() {
  const { data }: any = useRouteError();
  console.log(data)

  return (
    <>
      <PartnumPlaceholder />
      <div className={'error-block'}>
        { data.code && <h1>{ data.code }</h1> }
        <h3>{ data.message }</h3>
      </div>
    </>
  );
}