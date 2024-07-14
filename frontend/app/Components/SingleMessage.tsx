import { clsx } from "clsx";

type Props = {
  timestamp: Date;
  message: string;
  username?: string;
  response: boolean;
};

export default async function SingleMessage(props: Props) {
  return (
    <div className={clsx("w-full flex", !props.response && "justify-end")}>
      <div
        className={clsx(
          "m-2 pl-4 pt-2 pb-2 p-7 text-sm  rounded-full border border-spacing-2 flex flex-col ",
          !props.response ? "bg-blue-700 text-white" : "bg-slate-500 text-white"
        )}
      >
        <text className="decoration-sky-50 text-[10px]">
          {props.timestamp.toLocaleString().toString()}
        </text>
        <text>{props.message}</text>
      </div>
    </div>
  );
}
