from marvin import Bot
import asyncio


async def todo_main():

    todo_bot = await Bot.load("Taylor's Todo Bot")

    response = await todo_bot.say("I need to start the Andrew Ng course on prompt engineering.")
    
    return response

if __name__ == "__main__":

    response = asyncio.run(todo_main())

    print(response.content)



