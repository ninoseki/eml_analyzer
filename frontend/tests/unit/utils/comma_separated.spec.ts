import { describe, expect, it } from "vitest"

import { toCommaSeparatedString } from "@/utils/commaSeparated"

describe("#toCommaSeparatedString", function () {
  it("returns comma separated string", function () {
    const values = ["a", "b", "c"]
    expect(toCommaSeparatedString(values)).toEqual("a, b, c")
  })
})
