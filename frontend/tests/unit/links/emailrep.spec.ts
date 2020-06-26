import { EmailRep } from "@/links/emailrep";

describe("EmailRep", function () {
  const subject = new EmailRep();

  describe("#type", function () {
    it("equals to email", function () {
      expect(subject.type).toEqual("email");
    });
  });

  describe("#href", function () {
    it("returns URL", function () {
      const value = "foo@example.com";
      expect(subject.href(value)).toEqual(
        "https://emailrep.io/foo@example.com"
      );
    });
  });
});
