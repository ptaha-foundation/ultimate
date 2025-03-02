'use server'

import { API_ADDR } from '@/app/config';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

function convert_to_dict(list) {
  let dict = {};
  for (const i in list) {
    let {id, ...other} = list[i];
    dict[id] = other;
  };
  return dict;
}

export default async function getLotsData() {
  const cookieStore = await cookies();
  let token = cookieStore.get('access').value;

  let [lot_list_res, fuel_types_res, oil_bases_res] = [undefined, undefined, undefined];

  try {
    const lot_list_req = fetch(API_ADDR + '/trade/lots/', {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + token,
      }
    });
    const fuel_types_req = fetch(API_ADDR + '/trade/fuel-types/', {
      headers: {
        "Authorization": "Bearer " + token,
      }
    });
    const oil_bases_req = fetch(API_ADDR + '/trade/oil-bases/', {
      headers: {
        "Authorization": "Bearer " + token,
      }
    });
    [lot_list_res, fuel_types_res, oil_bases_res] =
      await Promise.all([lot_list_req, fuel_types_req, oil_bases_req]);
  } catch {
    await redirect(`/down?err=${encodeURIComponent("Неполадки с сервисом, попробуйте подключиться позже")}`);
  }

  const statuses = [lot_list_res.status, fuel_types_res.status, oil_bases_res.status];
  if (Math.floor(statuses[0]/100) != 2) {
    const err = await lot_list_res.json();
    await redirect(`/down?err=${encodeURIComponent(err.detail)}`);
  }
  if (Math.floor(statuses[1]/100) != 2) {
    const err = await fuel_types_res.json();
    await redirect(`/down?err=${encodeURIComponent(err.detail)}`);
  }
  if (Math.floor(statuses[2]/100) != 2) {
    const err = await oil_bases_res.json();
    await redirect(`/down?err=${encodeURIComponent(err.detail)}`);
  }

  const [lot_list, fuel_types_raw, oil_bases_raw] =
    await Promise.all([lot_list_res.json(), fuel_types_res.json(), oil_bases_res.json()]);

  const fuel_types = convert_to_dict(fuel_types_raw);
  const oil_bases = convert_to_dict(oil_bases_raw);
  return {
    "lot_list": lot_list,
    "fuel_types": fuel_types,
    "oil_bases": oil_bases,
  };
}
