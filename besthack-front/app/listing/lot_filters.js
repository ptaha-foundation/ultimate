'use client'

import { Toggle } from "@/components/ui/toggle"

export default function LotFilters(props) {
  const fuel_types = props.fuel_types;
  const oil_bases = props.oil_bases;

  let fuel_type_toggles = [];
  for (const i in fuel_types) {
    fuel_type_toggles.push(
      <Toggle 
        className="m-1" 
        variant="outline" 
        key={i}
        onPressedChange={
          (pressed) => {
            let filter = props.fuelTypeFilter.slice();
            if (pressed) {
              filter.push(parseInt(i))
            } else {
              const index = filter.indexOf(parseInt(i));
              if (index > -1) {
                filter.splice(index, 1);
              }
            }
            props.setFuelTypeFilter(filter);
          }
        }
      >
        {fuel_types[i].name}
      </Toggle>
    );
  };

  let regions = [];
  for (const i in oil_bases) {
    if (!regions.includes(oil_bases[i].region)) {
      regions.push(oil_bases[i].region);
    }
  };

  let region_toggles = [];
  for (const i in regions) {
    region_toggles.push(
      <Toggle
        className="m-1"
        variant="outline"
        key={i}
        onPressedChange={
          (pressed) => {
            let filter = props.oilBaseFilter.slice();
            if (pressed) {
              filter.push(regions[i])
            } else {
              const index = filter.indexOf(regions[i]);
              if (index > -1) {
                filter.splice(index, 1);
              }
            }
            props.setOilBaseFilter(filter);
          }
        }
      >{regions[i]}</Toggle>
    );
  };

  let base_name_toggles = [];
  for (const i in oil_bases) {
    base_name_toggles.push(
      <Toggle
        className="m-1"
        variant="outline"
        key={i}
        disabled={props.oilBaseFilter.length != 0 && !props.oilBaseFilter.includes(oil_bases[i].region)}
        onPressedChange={
          (pressed) => {
            let filter = props.oilBaseName.slice();
            if (pressed) {
              filter.push(oil_bases[i].name)
            } else {
              const index = filter.indexOf(oil_bases[i].name);
              if (index > -1) {
                filter.splice(index, 1);
              }
            }
            props.setOilBaseName(filter);
          }
        }
      >{oil_bases[i].name}</Toggle>
    );
  };

  return (
    <div className='bg-white sticky w-100 rounded-xl p-8 flex flex-col gap-8'>
      <h1 className='text-2xl'>Фильтры</h1>
      <div>
        <h2 className='text-xl'>Вид топлива</h2>
        {fuel_type_toggles}
      </div>
      <div>
        <h2 className='text-xl'>Регион нефтебазы, ФО</h2>
        {region_toggles}
      </div>
      <div>
        <h2 className='text-xl'>Название нефтебазы</h2>
        {base_name_toggles}
      </div>
    </div>
  );
}
