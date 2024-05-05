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
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-600">
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
        className="flex flex-col items-center justify-center
        w-96 h-96 bg-gray-700 rounded-xl shadow-2xl p-5"
      >
        <form className="flex max-w-md flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label
                className="text-white"
                htmlFor="username"
                value="Your username"
              />
            </div>
            <TextInput
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
                className="text-white"
                htmlFor="password"
                value="Your password"
              />
            </div>
            <TextInput
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex items-center gap-2">
            <Checkbox id="remember" />
            <Label className="text-white" htmlFor="remember">
              Remember me
            </Label>
          </div>

          <div id="login-button" className="flex items-center justify-around">
            <Button
              className="bg-green-700"
              type="button"
              onClick={() => {
                router.back();
              }}
            >
              Back
            </Button>
            <Button
              className="bg-green-700"
              type="button"
              onClick={() => navDashboard()}
            >
              Submit
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
