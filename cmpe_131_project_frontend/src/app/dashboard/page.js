import Sidebar from "./sidebar-components/sidebar";
import Calendar from "./calendar-components/calendar";

export default function Dashboard() {
  return (
    <div className="flex">
      <Sidebar />
      <Calendar />
    </div>
  );
}
