"use client";
import { useRouter } from "next/navigation";
import { Button } from "flowbite-react";
import { useEffect, useState } from "react";

export default function Home() {
  const router = useRouter();
  const [title, setTitle] = useState("Title");

  // useEffect(() => {
  //   fetch("http://localhost:8080/api/home")
  //     .then((response) => response.json())
  //     .then((data) => {
  //       setTitle(data.message);
  //     });
  // }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-slate-600">
      <div
        id="option-card"
        className="flex flex-col items-center justify-between w-96 h-96 bg-gray-700 rounded-xl shadow-2xl p-5"
      >
        <div
          id="home-header"
          className="flex items-center justify-center h-1/3 w-full"
        >
          <h1 className="text-center justify-center">Welcome to "{title}"</h1>
        </div>
        <div
          id="home-buttons"
          className="flex items-center justify-between w-96 h-96 bg-gray-700 rounded-xl"
        >
          <div
            id="create-account-component"
            className="flex items-center justify-center w-1/2 h-full"
          >
            <Button
              id="create-account-button"
              className="bg-green-700"
              onClick={() => {
                router.push("/create-account");
              }}
            >
              Create Account
            </Button>
          </div>
          <div
            id="signin-component"
            className="flex items-center justify-center w-1/2 h-full"
          >
            <Button
              id="signin-button"
              className="bg-green-700"
              onClick={() => {
                router.push("/login");
              }}
            >
              Sign In
            </Button>
          </div>
        </div>
      </div>
    </main>
  );
}
