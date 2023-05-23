import { useRouteError } from 'react-router-dom';
import ErrorLayout from "./ErrorLayout";

export default function ErrorComponent() {
  const { data }: any = useRouteError();

  return (
    <ErrorLayout code={data.code} message={data.message} />
  );
}