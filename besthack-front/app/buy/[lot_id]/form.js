'use client'

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { useState } from 'react';

import { Droplets } from 'lucide-react';

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

export default function BuyForm({props, onSubmit, currentLot, lot_list, fuel_types, oil_bases}) {
  const [tonnage, setTonnage] = useState(0);

  return (
    <div className='max-w-200 m-auto p-8 flex flex-col gap-4'>
      <h1 className="text-l m-4">Оформление заказа</h1>

      <div className='flex flex-col gap-2 bg-white rounded-xl w-full p-4'>
        <div className='flex gap-8 w-full h-24 p-4'>
          <div className='flex p-4 bg-slate-200 rounded-xl'>
            <div className='flex items-center'>
              <Droplets/>
              {fuel_types[currentLot.fuel_type].name}
            </div>
          </div>
          <div className='flex flex-col p-4 justify-center'>
            <div>
              лот №{currentLot.id}
            </div>
            <div className='text-xl nowrap'>
              {oil_bases[currentLot.oil_base].name} </div>
          </div>
          <div className='flex flex-col justify-center p-4'>
            <div className='text-xl'>{numberWithCommas(currentLot.total_price)} ₽</div>
            <div>Цена за тонну: {currentLot.price_per_ton} ₽</div>
          </div>
        </div>
        <div className="pl-4">
          Код КСС: {fuel_types[currentLot.fuel_type].ksss_code}<br/>
          Код КССС НБ: {oil_bases[currentLot.oil_base].ksss_code}<br/>
          Дата истечения лота: {currentLot.expiration_date}<br/>
          Доступно: {Math.floor(currentLot.available_volume)} тонн
        </div>
      </div>

      <div className='bg-white rounded-xl p-8'>
        <form action={onSubmit} className="space-y-8">
          <Label htmlFor="volume">Сколько тонн топлива необходимо заказать?</Label>
          <Input
            value={tonnage}
            onChange={e => setTonnage(e.target.value)}
            type="number"
            id="volume"
            name="volume"
            step="0.1"
            max={currentLot.available_volume}
            min="0.1"
          />
          <p>Общая стоимость топлива: {Math.floor(tonnage*currentLot.price_per_ton)} ₽</p>
          <Label>Способ доставки</Label>
          <RadioGroup name="delivery_type" defaultValue="option-one">
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="delivery" id="delivery" />
              <Label htmlFor="delivery">Доставка Лукойл - 1% от цены лота</Label>
            </div>
            <div className="flex items-center space-x-2">
              <RadioGroupItem value="pickup" id="pickup" />
              <Label htmlFor="pickup">Самовывоз</Label>
            </div>
          </RadioGroup>

          <Button type="submit">Отправить заказ</Button>
        </form>
      </div>
    </div>
  );
}
