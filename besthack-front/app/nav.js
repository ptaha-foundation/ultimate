import Link from 'next/link';
import { DoorOpen } from 'lucide-react';

import { Input } from "@/components/ui/input"
import { clearCookies } from "@/app/logout.js";

export default function Nav() {
  return (
    <div className='z-10 sticky top-0 bg-white w-full p-4 pl-10 pr-10'>
      <div className='max-w-400 flex justify-start items-center m-auto gap-12'>
        <img src='/logo.png' className='h-8'/>
        <Link href='/' className='text-xl'>Главная</Link>
        <div className='grow'></div>
        <Link href='' onClick={clearCookies} className='text-xl text-nowrap'><DoorOpen className="inline"/>Выход</Link>
      </div>
    </div>
  )
}
