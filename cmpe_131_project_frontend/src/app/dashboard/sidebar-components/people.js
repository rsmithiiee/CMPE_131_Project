"use client";
import { HiPlus } from "react-icons/hi";

export default function People() {
  return (
    <div className="flex flex-col justify-start bg-black p-2 w-1/5 item-center divide-y">
      <div className="flex items-center justify-center mb-3">
        <img
          src="/cat.jpg"
          width="40"
          height="40"
          alt="Cat"
          className="rounded-full hover:rounded-lg"
        />
      </div>
      <div className="flex flex-col">
        <div className="flex items-center justify-center mt-3">
          <img
            src="/cat.jpg"
            width="40"
            height="40"
            alt="Cat"
            className="rounded-full hover:rounded-lg"
          />
        </div>
        <div className="flex items-center justify-center mt-3">
          <img
            src="/cat.jpg"
            width="40"
            height="40"
            alt="Cat"
            className="rounded-full hover:rounded-lg"
          />
        </div>
        <div className="flex items-center justify-center mt-3">
          <img
            src="/cat.jpg"
            width="40"
            height="40"
            alt="Cat"
            className="rounded-full hover:rounded-lg"
          />
        </div>
        <div className="flex items-center justify-center mt-3">
          <button className="flex items-center justify-center size-10 rounded-full hover:rounded-lg hover:bg-gray-700">
            <HiPlus size={32} />
          </button>
        </div>
      </div>
    </div>
  );
}
