"use client"

import { processForm } from "./process_login"
 
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { useState } from "react";

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
import { Input } from "@/components/ui/input"

import { AlertCircle } from "lucide-react";
import { toast } from "sonner";

// TODO: максимальный лимит длины
const formSchema = z.object({
  username: z.string().min(2, {
    message: "Мин. длина: 2 символа",
  }).max(100, {
    message: "Макс.длина: 100 символов",
  }),
  password: z.string().min(2, {
    message: "Мин.длина: 2 символа",
  }).max(100, {
    message: "Макс.длина: 100 символов",
  }),
})
 
export default function ProfileForm() {
  const [errorMsg, setErrorMsg] = useState('');

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  })
 
  async function onSubmit(values) {
    const errMsg = await processForm(values);
    toast(errMsg, {
      icon: <AlertCircle/>
    })
  }
  return (
    <div>
      <img className="absolute top-4 left-4 w-64" src="/logo.png"/>
      <div className="bg-[url(/bg.png)] bg-cover w-screen h-screen p-16">
        <div className="max-w-100 m-auto p-4 rounded-xl bg-white text-xl">
          Вход
        </div>
        <div className="max-w-100 m-auto p-4 rounded-xl bg-white mt-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Логин</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormDescription>
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Пароль</FormLabel>
                    <FormControl>
                      <Input type="password" {...field} />
                    </FormControl>
                    <FormDescription>
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit">Войти</Button>
            </form>
          </Form>
        </div>
      </div>
    </div>
  )
}
