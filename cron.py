from functions import *
import asyncio


async def updateCron():
    ILBoardError, ILError, FGBoardError, FGError = update()
    if ILBoardError or ILError or FGBoardError or FGError:
        print("Error updating records, trying again")
        await updateCron()
    else:
        print("Recorddata successfully updated")


asyncio.run(updateCron())
