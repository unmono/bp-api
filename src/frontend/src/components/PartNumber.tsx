export type PartNumberType = {
  part_no: string,
  new_release: boolean,
  discontinued: boolean
}

export default function PartNumber(props: PartNumberType) {
  const boschThisNumber = (v: string) =>
    `${v.slice(0, 1)} ${v.slice(1, 4)} ${v.slice(4, 7)} ${v.slice(7, 10)}`;

  return(
    <div className={'part-number-block'}>
      <div className={'new-release'}>
        { props.new_release && 'New release'}
      </div>
      <div className={'discontinued'}>
        { props.discontinued && 'Discontinued'}
      </div>
      <div className={'part-number'}>
        { props.part_no && boschThisNumber(props.part_no) }
      </div>
    </div>
  );
}