import { test, expect } from '@playwright/test';

test.use({ ignoreHTTPSErrors: true });

test.describe('Company business class tests', () => {

  test('Favorite a station', async ({ page }) => {
    //favorite a station
    await page.goto('/stations');
    await page.locator('sm-station-tile').filter({ hasText: 'POP US contemporary pop hits' }).getByTitle('Add to My Stations').first().click();
    await page.getByRole('heading', { name: 'Filters Only show My Stations' }).locator('span').nth(1).click();
    await expect(page.getByRole('heading').filter({ hasText: 'Other ' })).toHaveCount(0);
    await expect(page.getByText('POP US contemporary pop hits').filter({ has: page.locator('.liked')})).toBeVisible();

    //unfavorite a station
    await page.locator("div", { has: page.locator('.liked') }).filter({ hasText: 'POP US contemporary pop hits' }).getByTitle('Add to My Stations').first().click();
    await expect(page.locator('sm-station-grid div').filter({ hasText: 'No results' })).toBeVisible();
  });

  // test('Create a mix', async ({ page }) => {
  //   //create the mix
  //   await page.goto('/mixes');
  //   await page.locator('a').filter({ hasText: 'New mix' }).click();
  //   await page.getByLabel('Name').fill('test mix');
  //   await page.getByRole('button', { name: 'ok' }).click();
  //   await expect(page.locator('a').filter({ hasText: 'test mix' })).toBeVisible();
  //   await page.waitForTimeout(3000);

  //   //add station to the mix
  //   await page.getByText('POP', { exact: true }).dragTo(page.locator('.empty-mix'));
  //   await expect(page.locator('sm-mix-station-list div').filter({ hasText: 'POP' }).nth(2)).toBeVisible();

  //   //delete the mix
  //   await page.locator('.menu-opener').click({delay:1000});
  //   await page.locator('a').filter({ hasText: 'Remove' }).hover();
  //   await page.locator('a').filter({ hasText: 'Remove' }).click();
  //   await page.getByRole('button', { name: 'ok' }).click();
  //   await expect(page.getByText('This mix contains no stations.')).toBeVisible();
  // });

  // test('Add a station to a mix', async ({ page }) => {
  //   await page.goto('/stations');
  //   await expect(page.getByText('No all')).toBeVisible();
  // });
  
  // test('Create a schdule', async ({ page }) => {
  //   await page.goto('/stations');
  //   await expect(page.getByText('No all')).toBeVisible();
  // });

  // test('Add a mix to a schedule', async ({ page }) => {
  //   await page.goto('/stations');
  //   await expect(page.getByText('No all')).toBeVisible();
  // });

  // test('Delete a schedule', async ({ page }) => {
  //   await page.goto('/mixes');
  //   await expect(page.locator('span').filter({ hasText: 'New mix' })).toBeVisible();
  // });

  // test('Delete a mix', async ({ page }) => {
  //   await page.goto('/schedules');
  //   await expect(page.locator('span').filter({ hasText: 'New schedule' })).toBeVisible();
  // });
});