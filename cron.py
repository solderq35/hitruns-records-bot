from functions import *
import asyncio
import time
import sys

LOG_LIMIT = 25


async def updateCron():
    ILBoardError, ILError, FGBoardError, FGError = await update()
    if ILBoardError or ILError or FGBoardError or FGError:
        print("Error updating records, trying again")
        await updateCron()
    else:
        print("Recorddata successfully updated")
        if (len(sys.argv) == 2) and sys.argv[1] == "--build":
            await updateLog(
                "update.log",
                str(int(time.time())) + " | railway container built" + "\n",
                10,
            )
        else:
            await updateLog(
                "update.log", str(int(time.time())) + " | railway cron job" + "\n", 10
            )


asyncio.run(updateCron())
