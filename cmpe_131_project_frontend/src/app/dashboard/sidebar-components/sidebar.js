import People from "./people";
import Group from "./group";
import Event from "./events";

export default function Sidebar() {
  return (
    <div className="flex bg-red-700 w-1/5 h-screen">
      <People />
      <div className="grid grid-rows-2 bg-black w-4/5 h-screen divide-y pad-2">
        <Group />
        <Event />
      </div>
    </div>
  );
}
