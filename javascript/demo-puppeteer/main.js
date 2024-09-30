const { console } = require("inspector");
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto("https://link3.cc/xiaoxiyouys");

  const element = await page.waitForSelector("div > .bt-cancel");
  await element.click();

  for (var i = 2578; i < 9999; i++) {
    const title = await page.waitForSelector("div > .shake_button");
    await title.click();
    await page.evaluate(() => localStorage.clear());


    const paddedNum = String(i).padStart(4, "0").toString();

    await page.type(".sms-code__input", paddedNum[0]);
    await page.type(".sms-code__input", paddedNum[1]);
    await page.type(".sms-code__input", paddedNum[2]);
    await page.type(".sms-code__input", paddedNum[3]);

    const ok = await page.waitForSelector(
      "#PEncryptedPopup > div.flexBC.pointer.b > div:nth-child(2) > span"
    );
    await ok.click();

    await page.evaluate(async () => {
      await new Promise(function (resolve) {
        setTimeout(resolve, 2000);
      });
    });

    const cancel = await page.waitForSelector(
      "#PEncryptedPopup > div.flexBC.pointer.b > div:nth-child(1) > span"
    );
    await cancel.click();
  }

  // await page.close();
  // await browser.close();
})();
