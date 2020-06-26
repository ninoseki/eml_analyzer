import { HybridAnalysis } from "@/links/hybridanalysis";

describe("HybridAanalysis", function () {
  const subject = new HybridAnalysis();

  describe("#type", function () {
    it("equals to sha256", function () {
      expect(subject.type).toEqual("sha256");
    });
  });

  describe("#href", function () {
    it("returns URL", function () {
      const value =
        "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f";
      expect(subject.href(value)).toEqual(
        `https://www.hybrid-analysis.com/search?query=${value}`
      );
    });
  });
});
