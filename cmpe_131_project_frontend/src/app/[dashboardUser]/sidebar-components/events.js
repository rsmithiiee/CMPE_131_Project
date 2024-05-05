"use client";
import { HiPlus } from "react-icons/hi";

export default function Event() {
  return (
    <div className="flex flex-col w-full">
      <li className="flex justify-between items-center w-full px-4 py-2 text-gray-900 font-lg bg-white border-b border-gray-200 dark:border-gray-600 drop-shadow">
        <label>Events</label>
        <button className="flex bg-white size-5 hover:bg-slate-300 rounded justify-center items-center">
          <HiPlus />
        </button>
      </li>
      <ul className="w-full h-full text-sm font-medium text-gray-900 bg-white border border-gray-200  dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div class="w-0 h-0 border-l-[10px] border-l-transparent border-b-[16px] border-b-emerald-600 border-r-[10px] border-r-transparent" />
          Event 1
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div class="w-0 h-0 border-l-[10px] border-l-transparent border-b-[16px] border-b-red-600 border-r-[10px] border-r-transparent" />
          Event 2
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div class="w-0 h-0 border-l-[10px] border-l-transparent border-b-[16px] border-b-blue-600 border-r-[10px] border-r-transparent" />
          Event 3
        </li>
        <li className="flex justify-start items-center gap-2 w-full px-4 py-2 border-b border-gray-200 rounded-t-lg dark:border-gray-600">
          <div class="w-0 h-0 border-l-[10px] border-l-transparent border-b-[16px] border-b-yellow-600 border-r-[10px] border-r-transparent" />
          Event 4
        </li>
      </ul>
    </div>
  );
}
