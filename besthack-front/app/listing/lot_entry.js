import Link from 'next/link'
import { Droplets } from 'lucide-react';

export default function LotEntry(props) {
  return (
    <Link href={'/buy/' + props.lot_id} className='flex gap-16 bg-white rounded-xl w-full h-24 p-4'>
      <div className='flex p-4 bg-slate-200 rounded-xl'>
        <div className='flex items-center'>
          <Droplets/>
          {props.fuel_type}
        </div>
      </div>
      <div className='flex p-4'>
        <div className='flex items-center'>
          Нефтебаза {props.oil_base}<br/>
          Регион: {props.oil_base_region}
        </div>
      </div>
      <div className='flex p-4'>
        <div className='flex items-center'>
          Доступно {Math.floor(props.available_volume)} тонн<br/>
          Истекает {props.expiration_date}
        </div>
      </div>
      <div className='flex p-4'>
        <div className='flex items-center'>
          {props.total_price}₽<br/>
          Цена за 1 тонну: {props.price_per_ton}₽
        </div>
      </div>
    </Link>
  );
}
