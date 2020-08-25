import { InQuest } from "@/links/inquest";

describe("InQuest", function () {
  const subject = new InQuest();

  describe("#type", function () {
    it("equals to sha256", function () {
      expect(subject.type).toEqual("sha256");
    });
  });

  describe("#href", function () {
    it("returns URL", function () {
      const hash = "8a8f93a0a4e4a709d73695accb2af068";
      expect(subject.href(hash)).toEqual(
        "https://labs.inquest.net/dfi/sha256/8a8f93a0a4e4a709d73695accb2af068"
      );
    });
  });
});
