import { describe, expect, it } from "vitest"

import { AnyRun } from "@/links/anyrun"

describe("AnyRun", function () {
  const subject = new AnyRun()

  describe("#type", function () {
    it("equals to sha256", function () {
      expect(subject.type).toEqual("sha256")
    })
  })

  describe("#href", function () {
    it("returns URL", function () {
      const hash = "8a8f93a0a4e4a709d73695accb2af068"
      expect(subject.href(hash)).toEqual(
        "https://app.any.run/submissions/#filehash:8a8f93a0a4e4a709d73695accb2af068"
      )
    })
  })
})
