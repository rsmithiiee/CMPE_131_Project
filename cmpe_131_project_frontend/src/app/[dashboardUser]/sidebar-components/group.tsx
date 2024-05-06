"use client";
import { HiPlus, HiDotsHorizontal } from "react-icons/hi";
import { useState, useRef, useEffect } from "react";
import { Modal, Dropdown } from "flowbite-react";
import type { CustomFlowbiteTheme } from "flowbite-react";

export default function Group({
  userName,
  setGroupUsers,
  setUserID,
  setGroupID,
  groupID,
  setShowFreeTime,
  showFreeTime,
}) {
  const selectGroup = useRef();
  const selectGroupName = useRef();
  const [modalInput, setModalInput] = useState({
    groupName: "",
    userName: "",
  });
  const [showAddGroupModal, setShowAddGroupModal] = useState(false);
  const [showGroupModal, setShowGroupModal] = useState(false);
  const groupIDList = useRef([]);
  const userlist = useRef([]);
  const [effectTrigger, setEffectTrigger] = useState(0);

  const userID = useRef(null);
  const [groupArray, setGroupArray] = useState([
    {
      group_id: "",
      group_name: "",
      usernames: [],
    },
  ]);

  const object = {
    username: userName,
  };
  useEffect(() => {
    async function fetchUserGroup() {
      const response = await fetch(
        "http://localhost:5000/api/retrieve_user_info",
        {
          method: "POST",
          body: JSON.stringify(object),
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      userID.current = data.user_id;
      setUserID(data.user_id);
      setGroupArray(data.groups);
    }

    fetchUserGroup();
  }, [effectTrigger]);

  const groupCards = groupArray.map((groupItem) => (
    <li
      key={groupItem.group_id}
      id={groupItem.group_id}
      className="flex h-auto focus:bg-slate-300 hover:bg-slate-300"
    >
      <button
        className="flex justify-start items-center w-full gap-2 px-4 py-2 border-b border-gray-200 dark:border-gray-600 focus:bg-slate-300 "
        id={groupItem.group_id}
        onClick={() => handleGroup(groupItem.usernames, groupItem.group_id)}
      >
        <div className="size-4 bg-emerald-600 rounded" />
        {groupItem.group_name}
      </button>
      <div className="flex justify-center items-center w-10">
        <button
          className="flex justify-center items-center h-full w-full border-b hover:bg-slate-300"
          onClick={() =>
            handleGroupMenu(groupItem.group_id, groupItem.group_name)
          }
        >
          <HiDotsHorizontal />
        </button>
      </div>

      <Modal show={showGroupModal} onClose={() => setShowGroupModal(false)}>
        <Modal.Header>Manage Users</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <form>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Enter User:
                </label>
                <input
                  type="text"
                  name="group-name"
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 
                            shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 
                            focus:ring-2 
                            focus:ring-inset focus:ring-slate-500 
                            sm:text-sm sm:leading-6"
                  value={modalInput.userName}
                  onChange={(e) =>
                    setModalInput({ ...modalInput, userName: e.target.value })
                  }
                  placeholder="Title"
                />
              </div>
            </form>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            disabled={modalInput.userName === ""}
            onClick={() => handleAddUser()}
          >
            Add
          </button>
          <button
            type="button"
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-black hover:bg-red-800 hover:text-white sm:col-start-1 sm:mt-0"
            onClick={() => handleDeleteUser()}
          >
            Delete
          </button>
        </Modal.Footer>
      </Modal>
    </li>
  ));

  function handleGroupMenu(group_id, group_name) {
    selectGroup.current = group_id;
    selectGroupName.current = group_name;
    setShowGroupModal(true);
  }

  async function handleAddUser() {
    const tempUserName = modalInput.userName;

    const object = {
      username: tempUserName,
      group_id: selectGroup.current,
    };
    const response = await fetch("http://localhost:5000/api/add_users_group", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("adding user");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);
    resetModal();
  }

  async function handleDeleteUser() {
    const tempUserName = modalInput.userName;

    const object = {
      username: tempUserName,
      group_id: selectGroup.current,
    };
    const response = await fetch(
      "http://localhost:5000/api/delete_user_group",
      {
        method: "POST",
        body: JSON.stringify(object),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    console.log("deleting user");
    const data = await response.json();
    const confirm = data.success;
    console.log(confirm);

    setEffectTrigger(effectTrigger + 1);
    resetModal();
  }

  function handleGroup(users, selectGroupID) {
    setGroupUsers(users);
    if (groupID == selectGroupID) {
      setShowFreeTime(!showFreeTime);
    }
    setGroupID(selectGroupID);
  }

  async function handleAddGroup() {
    const tempGroupName = modalInput.groupName;
    groupIDList.current.push(tempGroupName);
    const object = {
      user_id: userID.current,
      group_name: tempGroupName,
    };

    console.log("Add Group Obj: ", object);

    const response = await fetch("http://localhost:5000/api/create_group", {
      method: "POST",
      body: JSON.stringify(object),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log("group sent");
    const data = await response.json();
    const confirm = data.success;
    //groupIDList.current.push(data.group_id);
    console.log(confirm);

    setShowAddGroupModal(false);
    setEffectTrigger(effectTrigger + 1);
    resetModal();
  }

  function resetModal() {
    setModalInput({ ...modalInput, groupName: "", userName: "" });
  }

  return (
    <div className="flex flex-col w-full">
      <li className="flex justify-between items-center w-full px-4 py-2 text-gray-900 font-lg bg-white border-b border-gray-200 dark:border-gray-600 drop-shadow">
        <label>Groups</label>
        <button
          className="flex bg-white size-5 hover:bg-slate-300 rounded justify-center items-center"
          onClick={() => setShowAddGroupModal(true)}
        >
          <HiPlus />
        </button>
      </li>
      <ul className="w-full h-full text-sm font-medium text-gray-900 bg-white border border-gray-200  dark:bg-gray-700 dark:border-gray-600 dark:text-white">
        {groupCards}
      </ul>

      <Modal
        show={showAddGroupModal}
        onClose={() => setShowAddGroupModal(false)}
      >
        <Modal.Header>Create Group</Modal.Header>
        <Modal.Body>
          <div className="space-y-6">
            <form>
              <div className="mt-2">
                <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                  Group Name
                </label>
                <input
                  type="text"
                  name="group-name"
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 
                            shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 
                            focus:ring-2 
                            focus:ring-inset focus:ring-slate-500 
                            sm:text-sm sm:leading-6"
                  value={modalInput.groupName}
                  onChange={(e) =>
                    setModalInput({ ...modalInput, groupName: e.target.value })
                  }
                  placeholder="Title"
                />
              </div>
            </form>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <button
            type="button"
            className="inline-flex w-full justify-center bg-white rounded-md px-3 py-2 text-sm font-semibold text-black hover:text-white hover:bg-slate-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 sm:col-start-2"
            disabled={modalInput.groupName === ""}
            onClick={handleAddGroup}
          >
            Create
          </button>
          <button
            type="button"
            className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-black hover:bg-red-800 hover:text-white sm:col-start-1 sm:mt-0"
            onClick={() => setShowAddGroupModal(false)}
          >
            Cancel
          </button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
