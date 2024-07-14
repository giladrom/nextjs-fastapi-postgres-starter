"use client";

import { Message } from "../page";
import SingleMessage from "./SingleMessage";
import React, { useRef, useEffect } from "react";

type Props = {
  messages?: [Message];
  user_id?: string;
  user_name?: string;
};

export default function AllMessages(props: Props) {
  const bottomRef = useRef<null | HTMLDivElement>(null);

  // Make sure to scroll down so the most recent message is visible
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [props.messages]);

  return (
    <div className="w-full h-screen bg-gray-50 max-h-screen overflow-y-auto">
      {props.messages?.map((msg: Message) => {
        return (
          <div key={msg.id}>
            <SingleMessage
              message={msg.message}
              timestamp={new Date(msg.timestamp)}
              response={msg.sender_id != props.user_id}
            />
            <div ref={bottomRef} />
          </div>
        );
      })}
    </div>
  );
}
