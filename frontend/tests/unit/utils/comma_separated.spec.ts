import { toCommaSeparatedString } from "@/utils/comma_separated";

describe("#toCommaSeparatedString", function () {
  it("returns comma separated string", function () {
    const values = ["a", "b", "c"];
    expect(toCommaSeparatedString(values)).toEqual("a, b, c");
  });
});
