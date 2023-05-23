type ErrorLOProps = {
  code: number,
  message: string
}

export default function ErrorLayout(props: ErrorLOProps) {
  const {code, message} = props;

  return (
    <div className={'error-block'}>
      {code && <h1>{code}</h1>}
      <h3>{message}</h3>
    </div>
  );
}