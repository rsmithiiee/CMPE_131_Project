"use client";

import { Button, Checkbox, Label, TextInput } from "flowbite-react";

export default function Login() {
  //   const [title, setTitle] = useState("Title");

  //   useEffect(() => {
  //     fetch("http://localhost:8080/api/home")
  //       .then((response) => response.json())
  //       .then((data) => {
  //         setTitle(data.message);
  //       });
  //   }, []);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-600">
      <div
        id="option-card"
        className="flex flex-col items-center justify-center w-96 h-96 bg-gray-700 rounded-xl shadow-2xl p-5"
      >
        <form className="flex max-w-md flex-col gap-4">
          {/* <h>{title}</h> */}
          <div>
            <div className="mb-2 block">
              <Label className="text-white" htmlFor="text1" value="Your text" />
            </div>
            <TextInput id="text1" type="text" />
          </div>
          <Button className="bg-green-700" type="submit">
            Submit
          </Button>
        </form>
      </div>
    </div>
  );
}
