export default function CalendarDisplay() {
  return (
    <div className="p-5">
      <div className="flex flex-col w-full rounded-2xl bg-white text-black p-2">
        <div className="flex w-full h-20">
          <div className="w-7"></div>
          <div className="grid grid-cols-7 w-full h-16">
            <div>Sunday</div>
            <div>Monday</div>
            <div>Tuesday</div>
            <div>Wednesday</div>
            <div>Thursday</div>
            <div>Friday</div>
            <div>Saturday</div>
          </div>
        </div>
        <div className="flex w-full">
          <div className="w-7"></div>
          <div className="grid grid-cols-7 w-full h-16">
            <div>Sunday</div>
            <div>Monday</div>
            <div>Tuesday</div>
            <div>Wednesday</div>
            <div>Thursday</div>
            <div>Friday</div>
            <div>Saturday</div>
          </div>
        </div>
      </div>
    </div>
  );
}
