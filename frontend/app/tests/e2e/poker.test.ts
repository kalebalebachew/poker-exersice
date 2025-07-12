import { test, expect } from "@playwright/test";

test.describe("Poker Game", () => {
  test("should allow starting a new game", async ({ page }) => {
    // Navigate to the application
    await page.goto("http://localhost:3000");

    // Check if the title is visible
    await expect(page.locator("h1")).toContainText("Poker Game");

    // Check if the Start button is visible
    const startButton = page.getByRole("button", { name: "Start" });
    await expect(startButton).toBeVisible();

    // Click the Start button
    await startButton.click();

    // Check if the game is started (Reset button should be visible)
    const resetButton = page.getByRole("button", { name: "Reset" });
    await expect(resetButton).toBeVisible();

    // Check if player cards are dealt
    await expect(page.locator(".player-cards")).toBeVisible();
  });

  test("should allow performing actions", async ({ page }) => {
    // Navigate to the application
    await page.goto("http://localhost:3000");

    // Start the game
    await page.getByRole("button", { name: "Start" }).click();

    // Check if action buttons are visible
    await expect(page.getByRole("button", { name: "Check" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Fold" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Call" })).toBeVisible();
    await expect(page.getByRole("button", { name: "Bet" })).toBeVisible();

    // Perform a check action
    await page.getByRole("button", { name: "Check" }).click();

    // Check if the action is logged
    await expect(page.locator(".play-log")).toContainText("Check");
  });

  test("should display hand history", async ({ page }) => {
    // Navigate to the application
    await page.goto("http://localhost:3000");

    // Check if the hand history section is visible
    await expect(page.locator("text=Hand History")).toBeVisible();

    // Start a game
    await page.getByRole("button", { name: "Start" }).click();

    // Play a full hand (simplified for test)
    // Preflop
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();

    // Flop
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();

    // Turn
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();

    // River
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();
    await page.getByRole("button", { name: "Check" }).click();

    // Check if the hand appears in the hand history
    await expect(page.locator(".hand-history-item")).toBeVisible();
  });
});
