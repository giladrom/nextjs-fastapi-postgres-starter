import AllMessages from "./Components/AllMessages";
import MessageInput from "./Components/MessageInput";

export type User = {
  id: string;
  name: string;
};

export type Message = {
  id: string;
  sender_id: string;
  recipient_id: string;
  timestamp: string;
  message: string;
};

export const apiUrl = process.env.NEXT_PUBLIC_API_URL;
const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default async function Home() {
  const user: User = await fetch(`${apiUrl}/users/me`).then((res) => {
    return res.json();
  });

  // Get initial list of messages for the current user. This will be refreshed automatically when the "messages"
  // tag is invalidated (see refresh.ts).
  const messages: [Message] = await fetch(
    `${apiUrl}/messages/?user_id=${user.id}`,
    { next: { tags: ["messages"] } }
  ).then((res) => res.json());

  // Create a basic responsive chat interface
  return (
    <main className="flex min-h-screen flex-col items-center justify-center h-screen bg-white">
      <AllMessages messages={messages} user_id={user.id} />
      <MessageInput user_id={user.id} />
    </main>
  );
}
