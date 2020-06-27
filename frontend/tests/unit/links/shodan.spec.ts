import { Shodan } from "@/links/shodan";

describe("Shodan", function () {
  const subject = new Shodan();

  describe("#type", function () {
    it("equals to ip_address", function () {
      expect(subject.type).toEqual("ip_address");
    });
  });

  describe("#href", function () {
    it("returns URL", function () {
      const value = "1.1.1.1";
      expect(subject.href(value)).toEqual("https://www.shodan.io/host/1.1.1.1");
    });
  });
});
