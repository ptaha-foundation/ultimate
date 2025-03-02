'use client'

import Nav from '@/app/nav';

import { AlertCircle } from "lucide-react";

import Link from 'next/link';

export default function Listing(props) {
  return (
    <div>
      <Nav></Nav>
      <div className="p-16">
        <div className='flex flex-col max-w-120 m-auto p-8 bg-white rounded-xl gap-16'>
          <div className='flex text-xl text-red-400 justify-center'>
            Невозможно осуществить заказ<AlertCircle className="inline"/>
          </div>
          <div className="text-center">
            В лоте не осталось достаточно топлива
          </div>
          <Link href="/" className="text-center text-blue-500 underline">
            Вернуться на главную
          </Link>
        </div>
      </div>
    </div>
  );
}
