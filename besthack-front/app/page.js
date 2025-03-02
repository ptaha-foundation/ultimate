'use server'

import getLotsData from '@/app/get_lots_data';
import Listing from '@/app/listing/listing';

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function Page() {
  const cookieStore = await cookies();
  let accessToken = cookieStore.get('access');
  if (accessToken) {
    const data = await getLotsData();
    return (
      <Listing {...data}/>
    );
  }
  return redirect('/login');
}
