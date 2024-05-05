"use client";
import Sidebar from "./sidebar-components/sidebar";
import CalendarDisplay from "./calendar-components/calendar-display";
import { useState, useRef, useEffect } from "react";

export default function Dashboard({
  params,
}: {
  params: { dashboardUser: string };
}) {
  const [userName, setUserName] = useState(params.dashboardUser);
  const [userID, setUserID] = useState();
  //const [data, setData] = useState(null);

  return (
    <div className="flex">
      <Sidebar userName={userName} setUserID={setUserID} />
      <CalendarDisplay userID={userID} />
    </div>
  );
}
