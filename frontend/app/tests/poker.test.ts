import {
  formatCard,
  formatCards,
  formatHandType,
  getPositionName,
} from "../utils/poker";

describe("Poker Utilities", () => {
  // Test formatCard function
  describe("formatCard", () => {
    test("should format spades correctly", () => {
      expect(formatCard("As")).toBe("A♠");
      expect(formatCard("Ts")).toBe("T♠");
    });

    test("should format hearts correctly", () => {
      expect(formatCard("Ah")).toBe("A♥");
      expect(formatCard("2h")).toBe("2♥");
    });

    test("should format diamonds correctly", () => {
      expect(formatCard("Ad")).toBe("A♦");
      expect(formatCard("3d")).toBe("3♦");
    });

    test("should format clubs correctly", () => {
      expect(formatCard("Ac")).toBe("A♣");
      expect(formatCard("4c")).toBe("4♣");
    });

    test("should handle invalid input", () => {
      expect(formatCard("")).toBe("");
      expect(formatCard("A")).toBe("A");
      expect(formatCard("invalid")).toBe("invalid");
    });
  });

  // Test formatCards function
  describe("formatCards", () => {
    test("should format multiple cards correctly", () => {
      expect(formatCards(["As", "Kh"])).toBe("A♠ K♥");
      expect(formatCards(["Td", "2c", "3h"])).toBe("T♦ 2♣ 3♥");
    });

    test("should handle empty input", () => {
      expect(formatCards([])).toBe("");
      expect(formatCards(undefined)).toBe("");
    });
  });

  // Test formatHandType function
  describe("formatHandType", () => {
    test("should format hand types correctly", () => {
      expect(formatHandType("HighCard")).toBe("High Card");
      expect(formatHandType("Pair")).toBe("Pair");
      expect(formatHandType("TwoPair")).toBe("Two Pair");
      expect(formatHandType("ThreeOfAKind")).toBe("Three of a Kind");
      expect(formatHandType("Straight")).toBe("Straight");
      expect(formatHandType("Flush")).toBe("Flush");
      expect(formatHandType("FullHouse")).toBe("Full House");
      expect(formatHandType("FourOfAKind")).toBe("Four of a Kind");
      expect(formatHandType("StraightFlush")).toBe("Straight Flush");
      expect(formatHandType("RoyalFlush")).toBe("Royal Flush");
    });

    test("should return original string for unknown hand types", () => {
      expect(formatHandType("Unknown")).toBe("Unknown");
    });
  });

  // Test getPositionName function
  describe("getPositionName", () => {
    test("should return correct position names for 6-max table", () => {
      expect(getPositionName(0, 6)).toBe("BTN");
      expect(getPositionName(1, 6)).toBe("SB");
      expect(getPositionName(2, 6)).toBe("BB");
      expect(getPositionName(3, 6)).toBe("UTG");
      expect(getPositionName(4, 6)).toBe("MP");
      expect(getPositionName(5, 6)).toBe("CO");
    });

    test("should handle positions for non-standard table sizes", () => {
      expect(getPositionName(0, 4)).toBe("BTN");
      expect(getPositionName(1, 4)).toBe("SB");
      expect(getPositionName(2, 4)).toBe("BB");
      expect(getPositionName(3, 4)).toBe("P4");
    });
  });
});
