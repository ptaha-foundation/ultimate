import { API_ADDR } from '@/app/config';
import getLotsData from '@/app/get_lots_data';
import { cookies } from 'next/headers';
import Nav from '@/app/nav';
import BuyForm from './form';
import LotEntry from '@/app/listing/lot_entry';
import { redirect } from 'next/navigation';

export default async function BuyPage({params}) {
  const params_ready = (await params);
  const lotId = await params_ready.lot_id;
  const { lot_list, fuel_types, oil_bases } = await getLotsData();

  const currentLot = lot_list.find((lot) => lot.id === Number(lotId));

  if (!currentLot) {
    return <div>Лот не найден</div>;
  }

  async function onSubmit(formData) {
    'use server'

    const rawFormData = {
      lot: currentLot.id,
      volume: formData.get('volume'),
      delivery_type: formData.get('delivery_type'),
      delivery_address: 'TODO'
    }

    const cookieStore = await cookies();
    let token = cookieStore.get('access').value;

    console.log(rawFormData);

    const request = fetch(API_ADDR + '/trade/orders/', {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(rawFormData)
    });

    const response = await request;
    console.log(await response.text());
    console.log(response.status);
    if (Math.floor(response.status / 100) == 2) {
      redirect('/success');
    } else {
      redirect('/failure');
    }
  };

  return (
    <div>
      <Nav></Nav>
      <BuyForm
        onSubmit={onSubmit}
        currentLot={currentLot}
        lot_list={lot_list}
        fuel_types={fuel_types}
        oil_bases={oil_bases}
      />
    </div>
  );
}
