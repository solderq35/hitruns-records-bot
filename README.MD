## Hitruns Records Bot

Discord bot that provides an alternative (read-only) interface to the Hitman 3 leaderboard on speedrun.com as well as additional functionality.

For a more lightweight version of this as a website, visit the Hitruns Top Times site here: https://github.com/solderq35/hitruns-top-times/

Includes:

- Leaderboards for any given map / category (faster than going through speedrun.com itself)
- List of all records from oldest to newest for historical tracking
- Full game theoretical Sum of Bests based on individual level best times
- Video links included for all runs, and also a [Time Calc](https://solderq35.github.io/fg-time-calc/) link is included for full game runs

Based on Juliend10's work. I just moved this bot onto [Railway](https://railway.app/) for cloud based hosting.

**Local Environment**

- Run `pip3 install -r requirements.txt`
- Run `pip3 freeze > requirements.txt` to save library dependencies (only if you need to add a library or change dependencies for any other reason)
- Create a `.env` file with your Discord token listed as `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
- Run `python main.py`
- Make sure you have Python 3.8 (or 3.9 I think works) installed locally and in your PATH (for Windows)

**Remote Environment**

- Dependencies should be handled by `requirements.txt`
- Deploy on [Railway](https://railway.app/)
  - Add [Railway variable](https://docs.railway.app/develop/variables) for `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
  - I believe the default Python version on Railway is 3.8. (See [this link](https://nixpacks.com/docs/providers/python) for more info)

### Usage Instructions

Add the bot to your own Discord server with [this URL](https://discord.com/api/oauth2/authorize?client_id=1048593224735932508&permissions=2147486720&scope=bot%20applications.commands) or you can also DM it at `Hitruns Records Bot#1656`.

Commands:

- `!updateRecords`
  - Updates the database of records by going through speedrun.com's API
  - Can take a few minutes, please be patient!
  - **NOTE**: `!records <map> <rating>` and `!records <full game category> <rating>` (commands below) will still fetch the latest runs even if you haven't run `!updateRecords` in a while, but the other commands listed here will need `!updateRecords` to ensure the latest runs are fetched
  - Restarting container on Railway will retain whatever local `.json` files were in the container, but a redeploy will reset the `.json` files to what is in this Git Repo, until you run `!updateRecords` again
    - Potential future TODO: Look into migrating those `.json` files onto a cloud provider with Nonrelational database, like AWS DynamoDB or MongoDB
- `!records <level> <rating>`
  - Returns all records for a single level and rating, sorted fastest to slowest
  - Level names (either of the two options below will work):
    - Destination (ex: `!records dubai sa`. Note "haven", "ambrose", "romania" as arguably minor exceptions)
    - Level mission name (ex: `!records showstopper sa/so`). Note that if the level mission title has a space in it, then you must surround it with quotes. Ex: `!records "a gilded cage" sa`
    - For specifics, check [data/levelDict.json](data/levelDict.json) file. Any sufficiently long substring of the full level name (that is long enough to uniquely identify a single level) will work
  - Rating values: `SA` and `SA/SO`
    - Must have the slash there for `SA/SO`
- `!records <full game category> <rating>`
  - Returns all records for a single full game category and rating, sorted fastest to slowest
  - Full Game Category:
    - Full Game Category name (ex: `!records trilogy sa/so`). Note that if the campaign mission title has a space in it, then you must surround it with quotes. Ex: `!records "season 1" sa`
    - For specifics, check [data/campaignDict.json](data/campaignDict.json) file. Any sufficiently long substring of the full game category level name (that is long enough to uniquely identify a single full game category) will work
  - Rating values: `SA` and `SA/SO`
    - Must have the slash there for `SA/SO`
- `!records untied <amount>`
  - Returns `<amount>` of untied records
  - `records untied all` or `records untied` (no amount specified) will return the maximum amount of untied records
- `!records all <amount>`
  - Returns `<amount>` of records, tied or not
  - `records all` (no amount specified will return the maximum amount of records)
- `!sobs`
  - Returns theoretical sum of bests based on individual level times

Note: `!updateRecords` might be sluggish to respond as it involves going through a lot of data. The other commands should respond fairly quickly.

### Screenshots

![updateRecords](https://media.discordapp.net/attachments/1018323831468851202/1048705618078351380/image.png)

![recordsfg](https://media.discordapp.net/attachments/1018323831468851202/1049091135022317589/image.png)

![recordsil](https://media.discordapp.net/attachments/1018323831468851202/1049091366594019438/image.png)

![recordsuntied](https://media.discordapp.net/attachments/1018323831468851202/1049090686437294242/image.png)

![recordsall](https://media.discordapp.net/attachments/1018323831468851202/1049090785984909362/image.png)

![sobs](https://media.discordapp.net/attachments/1018323831468851202/1048705959893139526/image.png)
