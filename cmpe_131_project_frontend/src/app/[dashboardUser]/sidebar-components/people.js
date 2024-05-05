"use client";
import { HiPlus } from "react-icons/hi";
import { use, useState } from "react";

export default function People({ users, userName }) {
  const otherUsers = users.slice(1);
  const userCards = otherUsers.map((user) => (
    <div
      key={user}
      className="flex bg-yellow-400 items-center justify-center mt-3 size-9 rounded-full hover:rounded-lg"
    >
      <b>{user.substring(0, 1)}</b>
    </div>
  ));
  return (
    <div className="flex flex-col justify-start items-center bg-black px-2 w-1/5 item-center divide-y">
      <div className="flex bg-yellow-400 items-center justify-center my-2 size-9 rounded-full hover:rounded-lg">
        <b>{userName[0]}</b>
      </div>

      <div className="flex flex-col items-center ">{userCards}</div>
    </div>
  );
}
