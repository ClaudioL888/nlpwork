import { test, expect } from "@playwright/test";

test.describe("Dashboard", () => {
  test("shows keyword form", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Digital Empathy Platform")).toBeVisible();
    await expect(page.getByPlaceholder("e.g., earthquake")).toBeVisible();
  });
});
