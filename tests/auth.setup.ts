import { test as setup, expect } from '@playwright/test';

const playeronlyAuthFile = 'playwright/.auth/playeronlyUser.json';
const companyAuthFile = 'playwright/.auth/companyUser.json';


let playeronlyUsername = "luistest022124"
let playeronlyPassword = "luistest";

let companyUsername = "luiscompany022224"
let companyPassword = "luistest";

setup('authenticate', async ({ page }) => {
    // Perform authentication steps
    await page.goto('https://sound-machine.com/login');
    await page.getByRole('button', { name: 'Accept' }).click();
    await page.getByLabel('Username/email').fill(companyUsername);
    await page.getByLabel('Password').fill(companyPassword);
    await page.getByRole('button', { name: 'Log In Now!' }).click();
    
    // Wait for the final URL to ensure that the cookies are actually set.
    await page.waitForURL('/stations');
  
    // End of authentication steps.
  
    await page.context().storageState({ path: companyAuthFile });
  });