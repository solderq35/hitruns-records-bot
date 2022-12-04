## Hitruns Records Bot
Discord bot that provides an alternative (read-only) interface to the Hitman 3 leaderboard on speedrun.com as well as additional functionality.

Includes:
- Leaderboards for any given map / category (faster than going through speedrun.com itself)
- List of all records from oldest to newest for historical tracking
- Full game theoretical Sum of Bests based on individual level best times

Based on Juliend10's work. I just moved this bot onto [Railway](https://railway.app/) for cloud based hosting.

### Setup Instructions
Run `pip3 install discord.py` (and do pip3 install for any other libraries as well you don't have). 

Run `pip3 freeze > requirements.txt` to save library dependencies for Railway.

Add [Railway variable](https://docs.railway.app/develop/variables) for DISCORD_TOKEN ([See Discord Token Documentation](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token))

Other Info: https://nixpacks.com/docs/providers/python

### Usage Instructions
Add the bot to your own Discord server with [this URL](https://discord.com/api/oauth2/authorize?client_id=1048593224735932508&permissions=2147486720&scope=bot%20applications.commands) or you can also DM it at `Hitruns Records Bot#1656`.

Commands:
- `!updateRecords`
  - Updates the database of records by going through speedrun.com's API
- `!records <map> <rating>`
  - Returns all records for a given map and rating, sorted fastest to slowest. 
  - Rating values: SA and SA/SO. 
  - Map names: Destination (ex: `records dubai sa`. Note "haven", "ambrose", "romania" as arguably minor exceptions). You can also give the map name as the campaign mission title (ex: "Showstopper". Note that if the campaign mission title has a space in it, then you must surround it with quotes. Ex: `!records "a gilded cage" sa`
- `!records untied <amount>`
  - Returns `<amount>` of untied records
- `!records all <amount>`
  - Returns `<amount>` of records, tied or not
- `!sobs`
  - Returns theoretical sum of bests based on individual level times

Note: `!updateRecords` might be sluggish to respond as it involves going through a lot of data. The other commands should respond fairly quickly.

### Screenshots
![updateRecords](https://media.discordapp.net/attachments/1018323831468851202/1048705618078351380/image.png)

![recordsuntied](https://media.discordapp.net/attachments/1018323831468851202/1048705812383682630/image.png)

![recordsall](https://media.discordapp.net/attachments/1018323831468851202/1049016192003739648/image.png)

![recordsMap](https://media.discordapp.net/attachments/1018323831468851202/1049015923132084335/image.png)

![sobs](https://media.discordapp.net/attachments/1018323831468851202/1048705959893139526/image.png)