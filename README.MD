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

## Usage Instructions

Add the bot to your own Discord server with [this URL](https://discord.com/api/oauth2/authorize?client_id=1048593224735932508&permissions=2147486720&scope=bot%20applications.commands) or you can also DM it at `Hitruns Records Bot#1656`.

### Commands
- `!records [all | all-new | untied | untied-new] <?amount>`
  - Retrieves records from all categories and filters them by tie status or sorts them chronologically by newest or oldest first. Will show the number of records specified by user
  - Example: `!records all-new 10` to get the latest 10 records
- `!records [{level} | {full game category}] <rating> <?amount>`
  - Retrieves current leaderboard (sorted by run time) for a given level or full game category and rating  
- `!sobs`
  - Returns theoretical sum of bests (for full game categories) based on individual level times
- `!updateRecords ?[all | all-new | untied | untied-new | sobs] <?amount>`
  - Updates json files in Railway container to ensure fast lookup for `!records [all | all-new | untied | untied-new] <amount>` and `sobs`
  - **NOTE**: `!records [{level} | {full game category}] <rating>` will still fetch the latest runs even if you haven't run `!updateRecords` in a while. The other commands listed will need to run `!updateData` first to ensure data is up to date
   - Might be sluggish to respond as it involves going through a lot of data. The other commands should respond fairly quickly.
   - Restarting container on Railway will retain whatever local `.json` files were in the container, but a redeploy will reset the `.json` files to what is in this Git Repo, until you run `!updateRecords` again
     - Potential future TODO: Look into migrating those `.json` files onto a cloud provider with Nonrelational database, like AWS DynamoDB or MongoDB

### Command Troubleshooting

- Command names (anything starting with exclamation mark) are case sensitive. Make sure to type `!updateRecords` with correct capitalization
- Arguments are case-insensitive
- Arguments must be provided in the order listed for the given command
- See [Arguments section](#Arguments) for more info on any given argument
- Nomenclature:
  - `< >`: Stand-in value, e.g. substitute the specific Hitman level name
  - `[ | ]`: Multiple options in the square brackets separated by the vertical line, pick one for that argument slot
  - `{ }`: Denotes a stand-in value inside an argument group (`[ | ]`)
  - `?`: Means the argument / argument group is optional

### Arguments

- `all`: Returns all records without filtering for tie status, sorting by oldest first
- `all-new`: Returns all records, sorting by newest first
- `untied`: Returns all untied records, sorting by oldest first
- `untied-new`: Returns all records, sorting by newest first
- `{level name}`: Level name. Choose from:
  - Destination (ex: `dubai`. Note "haven", "ambrose", "romania" as arguably minor exceptions)
  - Level mission name (ex: `showstopper`). 
  - Note that if the level mission title has a space in it, then you must surround it with quotes. Ex: `!records "a gilded cage" sa`
  - For specifics, check [data/levelDict.json](data/levelDict.json) file. Any sufficiently long substring of the full level name (that is long enough to uniquely identify a single level) will work
- `{full game category}` Full game category. (ex: `trilogy`). 
  - Note that if the campaign mission title has a space in it, then you must surround it with quotes. Ex: `!records "season 1" sa`
  - For specifics, check [data/campaignDict.json](data/campaignDict.json) file. Any sufficiently long substring of the full game category level name (that is long enough to uniquely identify a single full game category) will work
- `{rating}`: `SA`, `SA/SO` (`SASO` also accepted), or `Any%` (`any` also accepted), which stands for "Silent Assassin", "Silent Asassin Suit Only", Any%  respectively
- `<amount>`: Specifies how many runs are returned
  - Leaving this blank will result in the maximum amount of runs for the query being returned

### Screenshots / Examples

![updateRecords](https://media.discordapp.net/attachments/1018323831468851202/1048705618078351380/image.png)

![recordsfg](https://media.discordapp.net/attachments/1018323831468851202/1049091135022317589/image.png)

![recordsil](https://media.discordapp.net/attachments/1018323831468851202/1049091366594019438/image.png)

![recordsuntied](https://media.discordapp.net/attachments/1018323831468851202/1049090686437294242/image.png)

![recordsall](https://media.discordapp.net/attachments/1018323831468851202/1049090785984909362/image.png)

![sobs](https://media.discordapp.net/attachments/1018323831468851202/1048705959893139526/image.png)
