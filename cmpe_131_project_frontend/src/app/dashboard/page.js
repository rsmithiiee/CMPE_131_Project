"use client";
import Sidebar from "./sidebar-components/sidebar";
import CalendarDisplay from "./calendar-components/calendar-display";
import { useState, useRef } from "react";

export default function Dashboard() {
  const userID = useRef(1);
  return (
    <div className="flex">
      <Sidebar />
      <CalendarDisplay user_id={userID.current} />
    </div>
  );
}
