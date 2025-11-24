import { test, expect } from "@playwright/test";

test.describe("Search", () => {
  test("can toggle search tab", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: "Search" }).click();
    await expect(page.getByPlaceholder("Search events")).toBeVisible();
  });
});
