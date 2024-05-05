"use client";
import { useRouter } from "next/navigation";
import { Button, Checkbox, Label, TextInput, Alert } from "flowbite-react";
import { useState } from "react";
import { HiInformationCircle } from "react-icons/hi";

export default function CreateAccount() {
  const router = useRouter();
  const [userTaken, setUserTaken] = useState();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const navDashboard = async () => {
    const object = {
      first_name: firstName,
      last_name: lastName,
      username: username,
      password: password,
    };
    const response = await fetch("http://localhost:5000/api/create_account", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("Data sent");
    const data = await response.json();
    const userTaken = data.success;
    console.log(data);

    if (!userTaken) {
      console.log(data.message);
      router.push("/" + username);
    } else if (userTaken) {
      console.log(data.message);
      setUserTaken(true);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-600">
      {userTaken && (
        <Alert
          color="failure"
          icon={HiInformationCircle}
          className="fixed top-0"
        >
          <span className="font-medium">User Taken. Please Try Again.</span>
        </Alert>
      )}
      <div
        id="option-card"
        className="flex flex-col items-center justify-center w-96 h-96 bg-gray-700 rounded-xl shadow-2xl p-4"
      >
        <form className="flex max-w-md flex-col gap-4">
          <div>
            <div className="mb-2 block">
              <Label
                className="text-white"
                htmlFor="firstname"
                value="Your First Name"
              />
            </div>
            <TextInput
              id="firstname"
              type="firstname"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div>
            <div>
              <div className="mb-2 block">
                <Label
                  className="text-white"
                  htmlFor="lastname"
                  value="Your Last Name"
                />
              </div>
              <TextInput
                id="lastname"
                type="lastname"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
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
              value={username}
              onChange={(e) => setUsername(e.target.value)}
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
            <TextInput
              id="password1"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div id="create-account-button" className="grid grid-cols-2">
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
              onClick={navDashboard}
            >
              Submit
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
