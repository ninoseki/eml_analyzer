import { describe, expect, it } from "vitest"

import { Browserling } from "@/links/browserling"

describe("Browserling", function () {
  const subject = new Browserling()

  describe("#type", function () {
    it("equals to url", function () {
      expect(subject.type).toEqual("url")
    })
  })

  describe("#href", function () {
    it("returns URL", function () {
      const hash = "http://example.com"
      expect(subject.href(hash)).toEqual(
        "https://www.browserling.com/browse/win/7/ie/11/http%3A%2F%2Fexample.com"
      )
    })
  })
})
