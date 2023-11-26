import { describe, expect, it } from "vitest"

import { Crtsh } from "@/links/crtsh"

describe("Crtsh", function () {
  const subject = new Crtsh()

  describe("#type", function () {
    it("equals to domain", function () {
      expect(subject.type).toEqual("domain")
    })
  })

  describe("#href", function () {
    it("returns URL", function () {
      const value = "example.com"
      expect(subject.href(value)).toEqual("https://crt.sh/?q=example.com")
    })
  })
})
