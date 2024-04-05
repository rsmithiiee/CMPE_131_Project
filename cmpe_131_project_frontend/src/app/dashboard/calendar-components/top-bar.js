"use client";
import { HiChevronLeft, HiChevronRight } from "react-icons/hi";
import { Dropdown } from "flowbite-react";

export default function Topbar() {
  return (
    <div className="flex justify-between bg-black w-full h-14 py-1 px-5">
      <div className="flex justify-center items-center">
        <label className="text-white text-4xl">Month, Year</label>
      </div>
      <ul className="flex justify-evenly items-center gap-2">
        <li>
          <button className="flex justify-center items-center rounded hover:bg-gray-700">
            <HiChevronLeft size={28} />
          </button>
        </li>
        <li className="flex justify-center items-center">
          <select
            id="countries"
            className=" bg-white text-black text-md rounded-lg w-full p-1 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white "
          >
            <option value="day">Day</option>
            <option selected="week">Week</option>
            <option value="month">Month</option>
            <option value="year">Year</option>
          </select>
        </li>
        <li>
          <button className="flex justify-center items-center rounded hover:bg-gray-700">
            <HiChevronRight size={28} />
          </button>
        </li>
      </ul>
    </div>
  );
}
