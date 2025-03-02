'use client'

import { API_ADDR } from '@/app/config';
import LotEntry from '@/app/listing/lot_entry';

export default function LotList(props) {
  let entries = [];
  for (const i in props.lot_list) {
    const e = props.lot_list[i];
    if (e.status != 'confirmed') {
      continue;
    }
    if (!(props.fuelTypeFilter.includes(e.fuel_type) || props.fuelTypeFilter.length == 0)) {
      continue;
    }
    if (!(props.oilBaseFilter.includes(props.oil_bases[e.oil_base].region) || props.oilBaseFilter.length == 0)) {
      continue;
    }
    if (!(props.oilBaseName.includes(props.oil_bases[e.oil_base].name) || props.oilBaseName.length == 0)) {
      continue;
    }
    entries.push(
      <LotEntry 
        key={e.id}
        lot_id={e.id}
        expiration_date={e.expiration_date}
        oil_base={props.oil_bases[e.oil_base].name}
        oil_base_region={props.oil_bases[e.oil_base].region}
        fuel_type={props.fuel_types[e.fuel_type].name}
        available_volume={e.available_volume}
        price_per_ton={e.price_per_ton}
        total_price={e.total_price}
        status={e.status}
      />
    )
  };

  return (
    <div className='w-full flex flex-col gap-4 pt-6'>
      {entries}
    </div>
  )
}
