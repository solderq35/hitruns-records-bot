# Hitruns Records Bot

Discord bot that provides an alternative (read-only) interface to the Hitman 3 leaderboard on speedrun.com as well as additional functionality.

Includes:

- Leaderboards for any given level / full game category (faster than going through speedrun.com itself)
- List of all records from oldest to newest for historical tracking
- Filtering for untied vs tied runs
- Full game theoretical Sum of Bests based on individual level best times
- Video links included for all runs, and also a [Time Calc](https://solderq35.github.io/fg-time-calc/) link is included for full game runs

Credits: Although I've made a lot of improvements to this bot since, and also improved its reliability by using [Railway](https://railway.app/) for cloud based hosting, [Juliend10](https://www.speedrun.com/users/juliend10) was a major collaborator early into the bot's development.

For a more traditional leaderboard implementation, also check out:

- [HitRuns](https://hitruns.vercel.app/)
  - [GitHub Repo](https://github.com/solderq35/hitruns)

**Local Environment**

- Make sure you have Python 3.8 (or 3.9 I think works) installed locally and in your PATH (for Windows)
- Pip version (if relevant): pip 23.3.1, from Python 3.8
- Run `pip install -r requirements.txt`
- Run `pip freeze > requirements.txt` to save library dependencies (only if you need to add a library or change dependencies for any other reason)
- Create a `.env` file with your Discord token listed as `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
- Run `python main.py`
- Code formatting: `black ./` (from root directory of this repo)

**Remote Environment**

- Dependencies should be handled by `requirements.txt`
- Deploy on [Railway](https://railway.app/)
  - Add [Railway variable](https://docs.railway.app/develop/variables) for `DISCORD_TOKEN` ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))
  - I believe the default Python version on Railway is 3.8. (See [this link](https://nixpacks.com/docs/providers/python) for more info)
  - Set the start command to `python cron.py && python main.py` to ensure the data is updated before the bot starts
  - Set up a daily cron job to automatically update data by following https://bookmarklets.up.railway.app/cron-config/
    - Also helpful for cron job syntax: https://crontab.guru
      - For this app, I used https://crontab.guru/#0_12_*_*_* for a cron job every day at 12 PM UTC

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
  - Any sufficiently long substring of a `<level name>` or `<fullgame category>` will work, e.g. either `showstopper` or `paris` would be valid. See [data/levelDict.json](https://github.com/solderq35/hitruns-records-bot/blob/master/data/levelDict.json) and [data/campaignDict.json](https://github.com/solderq35/hitruns-records-bot/blob/master/data/campaignDict.json) for a full list of names
  - Valid `<rating>` inputs: `SA`, `SA/SO` (`SASO` also accepted), or `Any%` (`any` also accepted)
  - Unlike the other commands listed here, even if Recorddata has not been updated recently, this command will still return up-to-date results
- `!sobs`
  - Calculates theoretical best times for full game categories, by summing up individual level record times
- `!getLogs`
  - See when Recorddata was last updated (tracks both manual updates and cron job automated updates, which happen each day at 12 PM UTC)
- `!updateRecords`
  - Update Recorddata manually if you need more precision than last 24 hours
  - Can also be 'queued' with some other commands, e.g. `!updateRecords all-new <amount>`, or `!updateRecords sobs`

**Note**: Bot will be down for a minute or two at 12 PM UTC each day for data update

**Note**: `<amount>` is optional. If not set, the max amount of records will be returned

### Command / Argument Troubleshooting

- Command names (anything starting with `!`) are case sensitive. Make sure to type `!updateRecords` with correct capitalization
- Arguments are case-insensitive (any capitalization will work)
- Arguments must be provided in the same order as in the Commands list above
- `<amount>` argument is optional for every command (bot will default to maximum length)
- All arguments are generally optional for `!updateRecords`
- See Argument section below for more info

### Screenshots / Examples

![updateRecordsAllNew](https://media.discordapp.net/attachments/1113022395243036682/1203184450423226469/image.png?ex=65d02bd7&is=65bdb6d7&hm=03a2a2f519ac5b5bcd2765407c9bff95f30eaf30ec7cd2029671328430f13989)

![updateRecords](https://media.discordapp.net/attachments/1018323831468851202/1048705618078351380/image.png)

![recordsfg](https://media.discordapp.net/attachments/1018323831468851202/1049091135022317589/image.png)

![recordsil](https://media.discordapp.net/attachments/1018323831468851202/1049091366594019438/image.png)

![recordsilamount](https://media.discordapp.net/attachments/1113022395243036682/1203185389456592909/image.png?ex=65d02cb6&is=65bdb7b6&hm=031cd5da223075930e1a4897f413c54c8b71ce5c1e0a6cbb203d3f19dd5f5721)

![recordsuntied](https://media.discordapp.net/attachments/1018323831468851202/1203185817179258930/image.png?ex=65d02d1c&is=65bdb81c&hm=c0e2561d33ba17c749a2b8354b14fa2c2e10439e6e19a6a783c7099b9f874930)

![recordsall](https://media.discordapp.net/attachments/1113022395243036682/1203185721419112468/image.png?ex=65d02d06&is=65bdb806&hm=2257aa47a98168809835696d42b4683e9448d93ebc4d3f0e279fab3c02e4f95d)

![sobs](https://media.discordapp.net/attachments/1018323831468851202/1048705959893139526/image.png)

![getLogs](https://media.discordapp.net/attachments/1113022395243036682/1203878167841087578/image.png?ex=65d2b1ea&is=65c03cea&hm=2dea9d9d2dd877260ad47a0349d2b59ea6fa9754594ef7d73b9147e869729300&)

![docs](https://media.discordapp.net/attachments/1113022395243036682/1203881727236382720/image.png?ex=65d2b53a&is=65c0403a&hm=89d83ab152eec2a7d6688737149cdefbd2c09f2b22c27793230317dcb25f1b94&=)
