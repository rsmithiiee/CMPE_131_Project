"use client";
import { useRouter } from "next/navigation";
import { Button } from "flowbite-react";
import { useEffect, useState } from "react";

export default function Home() {
  const router = useRouter();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-black">
      <div
        id="option-card"
        className="flex flex-col items-center justify-between w-96 bg-white rounded-xl shadow-2xl p-7"
      >
        <div
          id="home-header"
          className="flex items-center justify-center w-full"
        >
          <h1 className="text-center text-6xl text-black justify-center">
            <b>AllSync</b>
          </h1>
        </div>
        <div
          id="home-buttons"
          className="flex items-center justify-between w-96 mt-10 rounded-xl"
        >
          <div
            id="create-account-component"
            className="flex flex-col items-center justify-end w-1/2 h-full pb-2 "
          >
            <button
              id="create-account-button"
              className="text-black font-semibold hover:bg-black hover:text-white p-2 rounded-xl"
              onClick={() => {
                router.push("/create-account");
              }}
            >
              Create Account
            </button>
          </div>
          <div
            id="signin-component"
            className="flex flex-col items-center justify-end w-1/2 h-full pb-2 "
          >
            <button
              id="signin-button"
              className="text-black font-semibold hover:bg-black hover:text-white p-2 rounded-xl"
              onClick={() => {
                router.push("/login");
              }}
            >
              Sign In
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
