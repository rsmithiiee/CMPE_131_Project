"use client";
import "./calendar-style.css";
import { useState, useEffect, useRef } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin, {
  Draggable,
  DropArg,
} from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";
import { Button, Checkbox, Modal } from "flowbite-react";

export default function CalendarDisplay({ userID, groupID, showFreeTime }) {
  const [effectTrigger, setEffectTrigger] = useState(0);
  const object = {
    user_id: userID,
    start_time: "",
    end_time: "",
  };

  useEffect(() => {
    async function fetchUserGroup() {
      const response = await fetch(
        "http://localhost:5000/api/retrieve_user_events",
        {
          method: "POST",
          body: JSON.stringify(object),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      setEventArray(data);
    }

    fetchUserGroup();
  }, [effectTrigger, userID]);

  useEffect(() => {
    async function fetchFreeTime() {
      const calendarApi = calendarRef.current.getApi();
      const view = calendarApi.view;
      const startDate = view.currentStart;
      const endDate = view.currentEnd;
      console.log("View: ", view);
      console.log(
        "Week Date: ",
        startDate.toISOString(),
        " : ",
        endDate.toISOString()
      );
      const objectFreeTime = {
        group_id: groupID,
        start_time: startDate.toISOString(),
        end_time: endDate.toISOString(),
      };
      console.log("Week Date object: ", objectFreeTime);

      const response = await fetch(
        "http://localhost:5000/api/retrieve_group_free_times",
        {
          method: "POST",
          body: JSON.stringify(objectFreeTime),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      let tempArray = [];
      for (let i = 0; i < data.length; i++) {
        let temp = {
          backgroundColor: "green",
          editable: false,
          start: data[i].start,
          end: data[i].end,
        };
        tempArray.push(temp);
      }
      console.log("temp: ", tempArray);
      setFreeTimeArray(tempArray);
    }

    fetchFreeTime();
  }, [effectTrigger, groupID]);

  const calendarRef = useRef(null);

  const [showAddModal, setShowAddModal] = useState(false);
  const [showEventModal, setShowEventModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [modalInput, setModalInput] = useState({
    titleInput: "",
    startInput: "",
    endInput: "",
    allDayInput: false,
  });
  const [eventDetails, setEventDetails] = useState({
    titleInput: "",
    startDate: "",
    endDate: "",
  });
  const startSelectTime = useRef("");
  const endSelectTime = useRef("");
  const selectEventID = useRef();

  const eventList = useRef([]);
  const [eventArray, setEventArray] = useState([
    {
      title: "",
      start: "",
      end: "",
      allDay: false,
      id: 0,
    },
  ]);

  const [freeTimeArray, setFreeTimeArray] = useState([
    {
      backgroundColor: "green",
      editable: false,
      start: "",
      end: "",
    },
  ]);

  const checkHandler = () => {
    setModalInput({ ...modalInput, allDayInput: !modalInput.allDayInput });
  };

  function isoParser(date) {
    const dateObj = new Date(date);
    const hours = String(dateObj.getHours()).padStart(2, "0");
    const minutes = String(dateObj.getMinutes()).padStart(2, "0");
    const time = hours + ":" + minutes;
    return { time, hours, minutes };
  }

  async function handleAddEvent() {
    const startTime = startSelectTime.current.replace(
      isoParser(startSelectTime.current).time,
      modalInput.startInput
    );
    const endTime = endSelectTime.current.replace(
      isoParser(endSelectTime.current).time,
      modalInput.endInput
    );

    const object = {
      user_id: userID,
      event_name: modalInput.titleInput,
      start_time: startTime,
      end_time: endTime,
    };
    console.log("event:", object);
    const response = await fetch("http://localhost:5000/api/create_event", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("adding event");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);

    setModalInput({
      ...modalInput,
      titleInput: "",
      startInput: "",
      endInput: "",
      allDayInput: false,
    });
    setShowAddModal(false);
  }

  async function handleEventChange(event) {
    const selectEvent = event.event;

    const object = {
      user_id: userID,
      event_id: selectEvent.id,
      event_name: selectEvent.title,
      start_time: selectEvent.startStr,
      end_time: selectEvent.endStr,
    };
    console.log("event:", object);
    const response = await fetch("http://localhost:5000/api/edit_event", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("move event");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);
  }

  function handleDataSelect(date) {
    startSelectTime.current = date.startStr;
    endSelectTime.current = date.endStr;

    setModalInput({
      ...modalInput,
      startInput: isoParser(date.startStr).time,
      endInput: isoParser(date.endStr).time,
    });
    setShowAddModal(true);
    setEffectTrigger(effectTrigger + 1);
  }

  function handelEventClick(event) {
    selectEventID.current = event.event.id;

    setEventDetails({
      ...eventDetails,
      titleInput: event.event.title,
      startDate: String(event.event.start),
      endDate: String(event.event.end),
    });

    setModalInput({
      ...modalInput,
      titleInput: event.event.title,
      startInput: isoParser(event.event.startStr).time,
      endInput: isoParser(event.event.endStr).time,
    });
    // console.log("Event Select Modal: ", modalInput);
    setShowEventModal(true);
  }

  async function handleDeleteEvent() {
    const object = {
      user_id: userID,
      event_id: selectEventID.current,
    };
    console.log("event:", object);
    const response = await fetch("http://localhost:5000/api/delete_event", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("delete event");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);

    setShowEventModal(false);
  }

  function handleEditModal() {
    const calendarApi = calendarRef.current.getApi();
    console.log("Open Event Modal");
    setShowEventModal(false);
    setShowEditModal(true);

    const event = calendarApi.getEventById(selectEventID.current);

    setModalInput({
      ...modalInput,
      titleInput: event.title,
      startInput: isoParser(event.startStr).time,
      endInput: isoParser(event.endStr).time,
    });
  }

  async function handleEditEvent() {
    const calendarApi = calendarRef.current.getApi();
    const event = calendarApi.getEventById(selectEventID.current);

    const startTime = event.startStr.replace(
      isoParser(event.startStr).time,
      modalInput.startInput
    );
    const endTime = event.endStr.replace(
      isoParser(event.endStr).time,
      modalInput.endInput
    );

    const object = {
      user_id: userID,
      event_id: selectEventID.current,
      event_name: modalInput.titleInput,
      start_time: startTime,
      end_time: endTime,
    };
    console.log("event:", object);
    const response = await fetch("http://localhost:5000/api/edit_event", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("edit event");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);

    setShowEditModal(false);
    setModalInput({
      ...modalInput,
      titleInput: "",
      startInput: "",
      endInput: "",
    });
    console.log("event log edit: ", eventList);
  }

  return (
    <div className="w-full h-screen p-8 bg-black overflow-auto">
      <div className="w-full p-5 bg-white rounded-lg">
        <FullCalendar
          ref={calendarRef}
          plugins={[dayGridPlugin, interactionPlugin, timeGridPlugin]}
          headerToolbar={{
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek",
          }}
          events={showFreeTime ? freeTimeArray : eventArray}
          contentHeight={"auto"}
          nowIndicator={true}
          editable={true}
          droppable={true}
          selectable={true}
          selectMirror={true}
          eventChange={(event) => handleEventChange(event)}
          select={(event) => handleDataSelect(event)}
          eventClick={(event) => handelEventClick(event)}
        />
      </div>

      <Modal show={showEventModal} onClose={() => setShowEventModal(false)}>
        <Modal.Header>{eventDetails.titleInput}</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
              Start Date: {eventDetails.startDate}
              <br />
              End Date: {eventDetails.endDate}
            </p>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            onClick={() => handleEditModal()}
          >
            Edit
          </button>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-red-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            onClick={() => handleDeleteEvent()}
          >
            Delete
          </button>
        </Modal.Footer>
      </Modal>

      <Modal show={showAddModal} onClose={() => setShowAddModal(false)}>
        <Modal.Header>Add Event</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <form>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Title
                </label>
                <input
                  type="text"
                  name="title"
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 
                            shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 
                            focus:ring-2 
                            focus:ring-inset focus:ring-slate-500 
                            sm:text-sm sm:leading-6"
                  value={modalInput.titleInput}
                  onChange={(e) =>
                    setModalInput({ ...modalInput, titleInput: e.target.value })
                  }
                  placeholder="Title"
                />
              </div>
              <div className="flex gap-4 mt-2">
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Start time:
                  </label>
                  <div className="flex justify-between gap-5">
                    <input
                      type="time"
                      id="start-time"
                      className="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-slate-500 focus:border-slate-500 block w-full p-2.5"
                      value={modalInput.startInput}
                      onChange={(e) =>
                        setModalInput({
                          ...modalInput,
                          startInput: e.target.value,
                        })
                      }
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    End time:
                  </label>
                  <input
                    type="time"
                    id="end-time"
                    className="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-slate-500 focus:border-slate-500 block w-full p-2.5"
                    value={modalInput.endInput}
                    onChange={(e) =>
                      setModalInput({ ...modalInput, endInput: e.target.value })
                    }
                    required
                  />
                </div>
              </div>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  All Day
                </label>
                <input
                  type="Checkbox"
                  checked={modalInput.allDayInput}
                  onChange={checkHandler}
                  className="rounded shadow-md"
                />
              </div>
            </form>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            disabled={modalInput.titleInput === ""}
            onClick={handleAddEvent}
          >
            Create
          </button>
          <button
            type="button"
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-black hover:bg-red-800 hover:text-white sm:col-start-1 sm:mt-0"
            onClick={() => setShowAddModal(false)}
          >
            Cancel
          </button>
        </Modal.Footer>
      </Modal>

      <Modal show={showEditModal} onClose={() => setShowEditModal(false)}>
        <Modal.Header>Edit Event</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <form>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Title
                </label>
                <input
                  type="text"
                  name="title"
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 
                            shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 
                            focus:ring-2 
                            focus:ring-inset focus:ring-slate-500 
                            sm:text-sm sm:leading-6"
                  value={modalInput.titleInput}
                  onChange={(e) =>
                    setModalInput({ ...modalInput, titleInput: e.target.value })
                  }
                  placeholder="Title"
                />
              </div>
              <div className="flex gap-4 mt-2">
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    Start time:
                  </label>
                  <div className="flex justify-between gap-5">
                    <input
                      type="time"
                      id="start-time"
                      className="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-slate-500 focus:border-slate-500 block w-full p-2.5"
                      value={modalInput.startInput}
                      onChange={(e) =>
                        setModalInput({
                          ...modalInput,
                          startInput: e.target.value,
                        })
                      }
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                    End time:
                  </label>
                  <input
                    type="time"
                    id="end-time"
                    className="bg-gray-50 border leading-none border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-slate-500 focus:border-slate-500 block w-full p-2.5"
                    value={modalInput.endInput}
                    onChange={(e) =>
                      setModalInput({ ...modalInput, endInput: e.target.value })
                    }
                    required
                  />
                </div>
              </div>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  All Day
                </label>
                <input
                  type="Checkbox"
                  checked={modalInput.allDayInput}
                  onChange={checkHandler}
                  className="rounded shadow-md"
                />
              </div>
            </form>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            disabled={modalInput.titleInput === ""}
            onClick={handleEditEvent}
          >
            Save
          </button>
          <button
            type="button"
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-black hover:bg-red-800 hover:text-white sm:col-start-1 sm:mt-0"
            onClick={() => setShowEditModal(false)}
          >
            Cancel
          </button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
