export const validatePartnum = (value: string) => {
  const re = new RegExp(/^[A-Z0-9]{10}$/);
  return re.test(value);
}