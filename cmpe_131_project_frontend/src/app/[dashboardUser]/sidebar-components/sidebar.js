import People from "./people.js";
import Group from "./group.tsx";
import { useState } from "react";

export default function Sidebar({
  userName,
  setUserID,
  setGroupID,
  groupID,
  setShowFreeTime,
  showFreeTime,
}) {
  const [groupUsers, setGroupUsers] = useState([]);

  return (
    <div className="flex bg-red-700 w-1/5 h-screen">
      <People users={groupUsers} userName={userName} />
      <div className=" bg-white w-4/5 h-screen divide-y pad-2">
        <Group
          userName={userName}
          setGroupUsers={setGroupUsers}
          setUserID={setUserID}
          setGroupID={setGroupID}
          groupID={groupID}
          setShowFreeTime={setShowFreeTime}
          showFreeTime={showFreeTime}
        />
      </div>
    </div>
  );
}
