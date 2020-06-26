import moment from "moment/moment";

export function secondsToHumanize(seconds: number): string {
  if (seconds === 0) {
    return "-";
  }
  const duration = moment.duration(seconds, "seconds");
  return duration.humanize();
}
