## Hitruns Records Bot

Bot that tracks new speedrun world records in Hitman 3 as well as creating theoretical sum of bests based on best individual level times. 

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

![sobs](https://media.discordapp.net/attachments/1018323831468851202/1048705959893139526/image.png)