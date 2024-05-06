"use client";
import { useRouter } from "next/navigation";
import { Button, Checkbox, Label, TextInput, Alert } from "flowbite-react";
import { useState } from "react";
import { HiInformationCircle } from "react-icons/hi";

export default function Login() {
  const router = useRouter();
  const [invalidAuth, setInvalidAuth] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navDashboard = async () => {
    const object = { username: username, password: password };
    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    const isAuth = data.success;
    console.log(data);

    if (isAuth == true) {
      console.log(data.message);
      router.push("/" + username);
    } else if (isAuth == false) {
      console.log(data.message);
      setInvalidAuth(true);
      setUsername("");
      setPassword("");
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-black">
      {invalidAuth && (
        <Alert
          color="failure"
          icon={HiInformationCircle}
          className="fixed top-0"
        >
          <span className="font-medium">Invalid Login. Please Try Again.</span>
        </Alert>
      )}
      <div
        id="option-card"
        className="flex flex-col items-center justify-between w-96 bg-white rounded-xl shadow-2xl p-7"
      >
        <form className="flex max-w-md flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label
                className="text-black"
                htmlFor="username"
                value="Your username"
              />
            </div>
            <TextInput
              className="ring-2 rounded-lg ring-black"
              id="username"
              type="username"
              placeholder="Bob"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <div className="mb-2 block">
              <Label
                className="text-black"
                htmlFor="password"
                value="Your password"
              />
            </div>
            <TextInput
              className="ring-2 rounded-lg ring-black"
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center gap-2">
            <Checkbox className="ring-2 ring-black" id="remember" />
            <Label className="text-black" htmlFor="remember">
              Remember me
            </Label>
          </div>

          <div id="login-button" className="flex items-center justify-around">
            <button
              className="text-black font-semibold hover:bg-black hover:text-white p-2 rounded-xl"
              type="button"
              onClick={() => {
                router.back();
              }}
            >
              Back
            </button>
            <button
              className="text-black font-semibold hover:bg-black hover:text-white p-2 rounded-xl"
              type="button"
              onClick={() => navDashboard()}
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
