type flagType = {
  sw: boolean
}

export default function (props: flagType) {
  const {sw} = props;
  return <span style={{fontFamily: 'Courier'}}>{sw ? '-': '+'}</span>
}