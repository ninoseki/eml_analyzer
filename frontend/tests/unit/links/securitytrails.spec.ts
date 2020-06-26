import { SecurityTrails } from "@/links/securitytrails";

describe("SecurityTrails", function () {
  const subject = new SecurityTrails();

  describe("#type", function () {
    it("equals to domain", function () {
      expect(subject.type).toEqual("domain");
    });
  });

  describe("#href", function () {
    it("returns URL", function () {
      const value = "example.com";
      expect(subject.href(value)).toEqual(
        "https://securitytrails.com/domain/example.com"
      );
    });
  });
});
