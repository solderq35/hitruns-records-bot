from functions import *
import asyncio
import time

LOG_LIMIT = 25


async def updateCron():
    ILBoardError, ILError, FGBoardError, FGError = await update()
    if ILBoardError or ILError or FGBoardError or FGError:
        print("Error updating records, trying again")
        await updateCron()
    else:
        print("Recorddata successfully updated")
        await updateLog(
            "update.log", str(int(time.time())) + " | cron job update" + "\n", 10
        )


asyncio.run(updateCron())
