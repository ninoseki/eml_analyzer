import dayjs from "dayjs";
import duration from "dayjs/plugin/duration";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(duration);
dayjs.extend(relativeTime);

export function secondsToHumanize(seconds: number): string {
  if (seconds === 0) {
    return "-";
  }
  const duration = dayjs.duration(seconds, "seconds");
  return duration.humanize(false);
}
