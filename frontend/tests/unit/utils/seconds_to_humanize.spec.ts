import { secondsToHumanize } from "@/utils/seconds_to_humanize";

describe("#secondsToHumanize", function () {
  it("returns humanized string", function () {
    expect(secondsToHumanize(60)).toEqual("a minute");
    expect(secondsToHumanize(120)).toEqual("2 minutes");
    expect(secondsToHumanize(150)).toEqual("3 minutes");
  });
});
