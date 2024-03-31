# Hitruns Records Bot

Discord bot that tracks Hitman 3 speedrun statistics not on speedrun.com, such as fetching latest world records, filtering records by tie status, and calculating sums of bests.

Includes:

- **Data Caching**: The bot runs a daily cron job to:
  1. Collect all needed record data from speedrun.com API for every level and category of Hitman 3
  2. Transform and store record data in the bot's own database under a condensed and simplified schema
     - This reduces the number of API calls that would otherwise be needed for calculating sum of bests or fetching the latest records across all levels
  - For more implementation / usage details, see [Setup](#setup) and [Commands](#commands) sections below. Manually updating the bot's database is also supported
- Sorting records chronologically (oldest to newest, or newest to oldest)
- Filtering for untied vs tied records
- Full game theoretical Sum of Bests based on individual level best times
- Leaderboards for any given level / full game category (faster than going through speedrun.com itself)
- Video links included for all runs, and also a [Time Calc](https://solderq35.github.io/fg-time-calc/) link is included for full game runs

Credits: Although I've made a lot of improvements to this bot since, and also improved its reliability by using [Railway](https://railway.app/) for cloud based hosting, [Juliend10](https://www.speedrun.com/users/juliend10) was a major collaborator early into the bot's development.

For a more traditional leaderboard implementation, also check out:

- [HitRuns](https://hitruns.vercel.app/)
  - [GitHub Repo](https://github.com/solderq35/hitruns)

## Setup

### Local Environment

- Make sure you have Python 3.8+ installed locally and in your PATH (for Windows)
- Pip version (if relevant): pip 23.3.1, from Python 3.8
- Run `pip install -r requirements.txt`
- Run `pip freeze > requirements.txt` to save library dependencies (only if you need to add a library or change dependencies for any other reason)
- Create a `.env` file with your Discord token listed as `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
- Run `python main.py`
- Code formatting: `black ./` (from root directory of this repo)

### Remote Environment

- Dependencies should be handled by `requirements.txt`
- Deploy on [Railway](https://railway.app/)
  - Add [Railway variable](https://docs.railway.app/develop/variables) for `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
  - I believe the default Python version on Railway is 3.8. (See [this link](https://nixpacks.com/docs/providers/python) for more info)
  - Set the start command to `python cron.py && python main.py` to ensure the data is updated before the bot starts
  - Set up a daily cron job to automatically update data by following https://bookmarklets.up.railway.app/cron-config/
    - Also helpful for cron job syntax: https://crontab.guru
      - I used [this specific config](https://crontab.guru/#0_12_*_*_*) for a cron job every day at 12 PM UTC

## Usage Instructions

Add the bot to your own Discord server with [this URL](https://discord.com/api/oauth2/authorize?client_id=1048593224735932508&permissions=2147486720&scope=bot%20applications.commands) or you can also DM it at `Hitruns Records Bot#1656`.

### Commands

You can also use `!docs` command to see this help menu in Discord itself.

- `!records all <amount>`
  - Returns both tied and untied records, sorted by oldest to newest
- `!records all-new <amount>`
  - Returns both tied and untied records, sorted by newest to oldest
- `!records untied <amount>`
  - Returns untied records, sorted by oldest to newest
- `!records untied-new <amount>`
  - Returns untied records, sorted by newest to oldest
- `!records <level / fullgame category> <rating> <amount>`
  - Returns a single leaderboard for a level / fullgame category and rating
  - Any substring of a `<level name>` or `<fullgame category>` long enough to uniquely identify it will work, e.g. either `showstopper` or `paris` would be valid. See [data/levelDict.json](https://github.com/solderq35/hitruns-records-bot/blob/master/data/levelDict.json) and [data/campaignDict.json](https://github.com/solderq35/hitruns-records-bot/blob/master/data/campaignDict.json) (or `!levelNames` and `!fgNames` discord commands) for a full list of names
  - Any level or fullgame category name you input that contains a space (e.g. `"season 3"` or `"a gilded cage"`) should be surrounded by quotes
  - Valid `<rating>` inputs: `sa`, `saso`, or `any
  - Unlike the other commands listed here, even if Recorddata (the bot's database) has not been updated recently, this command will still return up-to-date results
- `!sobs`
  - Calculates theoretical best times for full game categories, by summing up individual level record times
- `!getLogs`
  - See when Recorddata (the bot's database) was last updated (tracks both manual updates and cron job automated updates, which happen each day at 12 PM UTC)
- `!updateRecords`
  - Updates Recorddata (the bot's database) manually if you need more precision than last 24 hours
  - Can also be "queued" with some other commands, e.g. `!updateRecords all-new <amount>`, or `!updateRecords sobs`

**Note**: Bot will be down for a minute or two at 12 PM UTC each day for Recorddata (bot database) update

**Note**: `<amount>` is optional. If not set, the max amount of records will be returned

### Command / Argument Troubleshooting

- Command names (anything starting with `!`) are case sensitive. Make sure to type `!updateRecords` with correct capitalization
- Arguments are case-insensitive (any capitalization will work)
- Arguments must be provided in the same order as in the Commands list above
- `<amount>` argument is optional for every command (bot will default to maximum length)
- `!updateRecords` can be a bit slow to update, it's normal to have to wait a minute or two for it to complete
- All arguments are generally optional for `!updateRecords`

### Screenshots / Examples

![updateRecordsAllNew](https://i.ibb.co/nQ54dxK/recordsallnew.png)

![updateRecords](https://i.ibb.co/FJhS7Fy/updaterecords.png)

![recordsfg](https://i.ibb.co/fpJCGPp/recordsfg.png)

![recordsil](https://i.ibb.co/NpHNP6W/recordsil.png)

![recordsilamount](https://i.ibb.co/5c8z63Q/recordsilamount.png)

![recordsuntied](https://i.ibb.co/c1DxHjN/recordsuntied.png)

![recordsall](https://i.ibb.co/xS191j6/recordsall.png)

![sobs](https://i.ibb.co/WBjLB4j/sobs.png)

![getLogs](https://i.ibb.co/s6ZYHKt/getlogs.png)

![docs](https://i.ibb.co/WHQGq2Y/recordsdocs.png)
