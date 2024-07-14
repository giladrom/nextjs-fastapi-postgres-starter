"use client";

import React from "react";
import { apiUrl } from "../page";
import refresh from "../utils/refresh";

type Props = {
  user_id: string;
};

export default function MessageInput(props: Props) {
  const [input, setInput] = React.useState("");

  const onChangeHandler = (event: {
    target: { value: React.SetStateAction<String> };
  }) => {
    setInput(event.target.value as string);
  };

  const handleKeyDown = async (event: { key: string }) => {
    if (event.key === "Enter" && input.length > 0) {
      await fetch(`${apiUrl}/messages/`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
          sender_id: props.user_id.toString(),
        }),
      })
        .then((res) => {
          return res.json();
        })
        .catch((err) => {
          console.error(err);
        });

      setInput("");

      // Invalidate cache tag to retrieve latest messages from the server
      refresh();
    }
  };

  return (
    <>
      <div className="w-full flex flex-col">
        <input
          className="text-black p-4 border border-x-slate-500"
          maxLength={512}
          type="text"
          name="name"
          onChange={onChangeHandler}
          onKeyDown={handleKeyDown}
          value={input}
          placeholder="Type your message here and press Enter"
        />
      </div>
    </>
  );
}
