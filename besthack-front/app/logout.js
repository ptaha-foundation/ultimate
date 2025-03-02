'use server'

import { cookies } from 'next/headers';
import { redirect } from 'next/navigation'

export async function clearCookies() {
  const cookieStore = await cookies();
  cookieStore.delete('access');
  cookieStore.delete('refresh');
  return redirect('/login');
}
