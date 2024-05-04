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

export default function CalendarDisplay(user_id) {
  const calendarRef = useRef(null);
  const user = user_id;
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
  const eventID = useRef(1);

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

  function handleAddEvent() {
    const calendarApi = calendarRef.current.getApi();

    const startTime = startSelectTime.current.replace(
      isoParser(startSelectTime.current).time,
      modalInput.startInput
    );
    const endTime = endSelectTime.current.replace(
      isoParser(endSelectTime.current).time,
      modalInput.endInput
    );

    const tempEvent = {
      title: modalInput.titleInput,
      start: startTime,
      end: endTime,
      //allDay: modalInput.allDayInput,
      id: eventID.current,
    };

    eventList.current.push(tempEvent);
    console.log("event log add: ", eventList);

    calendarApi.addEvent(tempEvent);
    console.log(calendarApi.getEvents());
    setModalInput({
      ...modalInput,
      titleInput: "",
      startInput: "",
      endInput: "",
      allDayInput: false,
    });
    eventID.current++;
    setShowAddModal(false);
  }

  function handleEventChange(event) {
    const selectEvent = event.event;
    const selectEventId = selectEvent.id;
    const tempEvent = {
      title: selectEvent.title,
      start: selectEvent.startStr,
      end: selectEvent.endStr,
      allDay: selectEvent.allDay,
      id: selectEventId,
    };

    eventList.current[selectEventId] = tempEvent;
    console.log("event log: ", eventList);
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
  }

  function handelEventClick(event) {
    const calendarApi = calendarRef.current.getApi();
    selectEventID.current = event.event.id;
    const targetEvent = calendarApi.getEventById(event.event.id);
    const start = new Date(targetEvent.startStr);
    const end = new Date(targetEvent.endStr);
    setEventDetails({
      ...eventDetails,
      titleInput: targetEvent.title,
      startDate: String(start),
      endDate: String(end),
    });
    setShowEventModal(true);
  }

  function handleDeleteEvent() {
    const calendarApi = calendarRef.current.getApi();
    const event = calendarApi.getEventById(selectEventID.current);
    event.remove();
    eventList.current.splice(selectEventID.current, 1);
    setShowEventModal(false);
    console.log("event log delete: ", eventList);
    console.log(calendarApi.getEvents());
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

  function handleEditEvent() {
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

    event.setProp("title", modalInput.titleInput);
    event.setStart(startTime);
    event.setEnd(endTime);

    const tempEvent = {
      title: event.title,
      start: startTime,
      end: endTime,
      allDay: event.allDay,
      id: event.id,
    };

    eventList.current[event.id] = tempEvent;

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
