"use client";
import Link from "next/link";
import { Button, Checkbox, Label, TextInput } from "flowbite-react";

export default function Login() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-600">
      <div
        id="option-card"
        className="flex flex-col items-center justify-center w-96 h-96 bg-gray-700 rounded-xl shadow-2xl p-5"
      >
        <form className="flex max-w-md flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label
                className="text-white"
                htmlFor="email1"
                value="Your email"
              />
            </div>
            <TextInput
              id="email1"
              type="email"
              placeholder="name@flowbite.com"
              required
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label
                className="text-white"
                htmlFor="password1"
                value="Your password"
              />
            </div>
            <TextInput id="password1" type="password" required />
          </div>
          <div className="flex items-center gap-2">
            <Checkbox id="remember" />
            <Label className="text-white" htmlFor="remember">
              Remember me
            </Label>
          </div>
          <div id="login-button" className="grid grid-cols-2">
            <Link href="/">
              <Button className="bg-green-700" type="submit">
                Back
              </Button>
            </Link>
            <Button className="bg-green-700" type="submit">
              Submit
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
