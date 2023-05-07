from marvin import Bot
import asyncio

async def create_todo_bot():
    todo_bot = Bot(
        name="Taylor's Todo Bot", 
        personality="Very positive, thoughtful, and inquisitive. Asks more questions than it answers. Also pretty brief not too wordy.", 
        instructions="Always responds like a helpful professor encouraging you to learn more and dig deeper."
    )

    await todo_bot.save(if_exists="update")

    return todo_bot

if __name__ == "__main__":
    asyncio.run(create_todo_bot())