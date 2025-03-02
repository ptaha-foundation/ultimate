import Link from 'next/link';

export default async function ServiceDown({params, searchParams}) {
  console.log(searchParams);
  return (<div>
    Неполадки с сервисом, попробуйте зайти попозже<br/>
    <Link href="/" className="text-blue-900 underline">Попробовать ещё раз</Link>
  </div>);
}
