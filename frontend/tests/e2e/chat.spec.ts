import { test, expect } from "@playwright/test";

test.describe("Chat", () => {
  test("can toggle chat tab", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Chat" }).click();
    await expect(page.getByText("Room")).toBeVisible();
  });
});
