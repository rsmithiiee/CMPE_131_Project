"use client";
import { HiPlus } from "react-icons/hi";

export default function Group() {
  return (
    <div className="flex flex-col w-full">
      <li className="flex justify-between items-center w-full px-4 py-2 text-gray-900 font-lg bg-white border-b border-gray-200 dark:border-gray-600 drop-shadow">
        <label>Groups</label>
        <button className="flex bg-white size-5 hover:bg-slate-300 rounded justify-center items-center">
          <HiPlus />
        </button>
      </li>
      <ul className="w-full h-full text-sm font-medium text-gray-900 bg-white border border-gray-200  dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div className="size-4 bg-emerald-600 rounded" />
          Group 1
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div className="size-4 bg-red-600 rounded" />
          Group 2
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div className="size-4 bg-blue-600 rounded" />
          Group 3
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div className="size-4 bg-yellow-600 rounded" />
          Group 4
        </li>
      </ul>
    </div>
  );
}
