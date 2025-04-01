import discord
from discord.ext import commands
import openai
import pip
import sys
import subprocess

subprocess.run([sys.executable, '-m', 'pip', 'install','openai ==0.28'])


# Set up your OpenAI API key
openai.api_key = 'INSERT API KEY'

#Set up BOT Token
TOKEN = 'INSERT DISCORD BOT TOKEN'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Set up logging
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


# Movie database with 10 movies in each genre
movies = {
    "horror": [
        {"id": 1, "name": "Alien", "rating": 7.5, "ratings": []},
        {"id": 2, "name": "Hereditary", "rating": 7.3, "ratings": []},
        {"id": 3, "name": "Psycho", "rating": 7.5, "ratings": []},
        {"id": 4, "name": "It", "rating": 7.4, "ratings": []},
        {"id": 5, "name": "Jaws", "rating": 7.7, "ratings": []},
        {"id": 6, "name": "Dracula", "rating": 8.0, "ratings": []},
        {"id": 7, "name": "Halloween", "rating": 7.8, "ratings": []},
        {"id": 8, "name": "Sinister", "rating": 6.8, "ratings": []},
        {"id": 9, "name": "Carrie", "rating": 7.1, "ratings": []},
        {"id": 10, "name": "Insidious", "rating": 6.8, "ratings": []}
    ],
    "comedy": [
        {"id": 1, "name": "If", "rating": 7.7, "ratings": []},
        {"id": 2, "name": "Superbad", "rating": 7.6, "ratings": []},
        {"id": 3, "name": "Thelma", "rating": 6.9, "ratings": []},
        {"id": 4, "name": "Anchorman", "rating": 7.2, "ratings": []},
        {"id": 5, "name": "Deadpool", "rating": 7.3, "ratings": []},
        {"id": 6, "name": "Bridesmaids", "rating": 6.8, "ratings": []},
        {"id": 7, "name": "Zoolander", "rating": 6.5, "ratings": []},
        {"id": 8, "name": "Challengers", "rating": 7.0, "ratings": []},
        {"id": 9, "name": "Popeye", "rating": 7.1, "ratings": []},
        {"id": 10, "name": "Wonka", "rating": 6.9, "ratings": []}
    ],
    "romance": [
        {"id": 1, "name": "Her", "rating": 7.8, "ratings": []},
        {"id": 2, "name": "Touch", "rating": 7.8, "ratings": []},
        {"id": 3, "name": "Grease", "rating": 8.0, "ratings": []},
        {"id": 4, "name": "Twilight", "rating": 7.4, "ratings": []},
        {"id": 5, "name": "Titanic", "rating": 7.8, "ratings": []},
        {"id": 6, "name": "Elemental", "rating": 7.0, "ratings": []},
        {"id": 7, "name": "After", "rating": 7.6, "ratings": []},
        {"id": 8, "name": "Ghosted", "rating": 7.7, "ratings": []},
        {"id": 9, "name": "Casablanca", "rating": 7.0, "ratings": []},
        {"id": 10, "name": "Footloose", "rating": 7.6, "ratings": []}
    ],
    "action": [
        {"id": 1, "name": "Rocky-1", "rating": 8.1, "ratings": []},
        {"id": 2, "name": "Gladiator", "rating": 8.5, "ratings": []},
        {"id": 3, "name": "Rambo", "rating": 7.4, "ratings": []},
        {"id": 4, "name": "Dune", "rating": 9.0, "ratings": []},
        {"id": 5, "name": "Taken-2", "rating": 8.2, "ratings": []},
        {"id": 6, "name": "Inception", "rating": 8.8, "ratings": []},
        {"id": 7, "name": "Twister", "rating": 8.7, "ratings": []},
        {"id": 8, "name": "Ronin", "rating": 8.4, "ratings": []},
        {"id": 9, "name": "Ambulance", "rating": 7.9, "ratings": []},
        {"id": 10, "name": "Skyfall", "rating": 7.8, "ratings": []}
    ],
    "drama": [
        {"id": 1, "name": "Aloha", "rating": 8.8, "ratings": []},
        {"id": 2, "name": "Ferrari", "rating": 9.2, "ratings": []},
        {"id": 3, "name": "Bable", "rating": 8.8, "ratings": []},
        {"id": 4, "name": "Reptile", "rating": 9.3, "ratings": []},
        {"id": 5, "name": "Brothers", "rating": 7.7, "ratings": []},
        {"id": 6, "name": "Parasite", "rating": 8.6, "ratings": []},
        {"id": 7, "name": "Whiplash", "rating": 8.5, "ratings": []},
        {"id": 8, "name": "Zodiac", "rating": 8.1, "ratings": []},
        {"id": 9, "name": "Napolean", "rating": 8.0, "ratings": []},
        {"id": 10, "name": "Enemy", "rating": 8.3, "ratings": []}
    ]
}

# Define the intents
intents = discord.Intents.default()
intents.message_content = True

# Create a bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to get movie synopsis from ChatGPT
async def get_movie_synopsis(movie_name):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Provide a brief synopsis for the movie '{movie_name}'"}
        ],
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} is now ready.')

@bot.command()
async def recommend(ctx, *, genre: str = None):
    if genre is None:
        await ctx.send("Please specify a genre. Usage: !recommend <genre>")
        return

    print(f'Received command: recommend with genre {genre}')
    genre = genre.lower()
    if genre not in movies:
        await ctx.send(
            "Sorry, I don't have recommendations for that genre. Please choose from horror, comedy, romance, action, or drama.")
        return

    movie_list = sorted(movies[genre], key=lambda x: x['rating'], reverse=True)
    recommendations = "\n".join([movie['name'] for movie in movie_list])
    await ctx.send(f"Top {genre} movies:\n{recommendations}")

@bot.command()
async def rate(ctx, movie_name: str = None, rating: float = None):
    if movie_name is None or rating is None:
        await ctx.send("Please specify a movie name and rating. Usage: !rate <movie_name> <rating>")
        return

    print(f'Received command: rate for movie {movie_name} with rating {rating}')
    found = False
    for genre, movie_list in movies.items():
        for movie in movie_list:
            if movie['name'].lower() == movie_name.lower():
                movie['ratings'].append(rating)
                movie['rating'] = sum(movie['ratings']) / len(movie['ratings'])
                await ctx.send(f"The new average rating for {movie['name']} is {movie['rating']:.1f}.")
                found = True
                break
        if found:
            break

    if not found:
        await ctx.send(f"Sorry, I couldn't find a movie named '{movie_name}'.")

@bot.command()
async def synopsis(ctx, *, movie_name: str = None):
    if movie_name is None:
        await ctx.send("Please specify a movie name. Usage: !synopsis <movie_name>")
        return

    print(f'Received command: synopsis for movie {movie_name}')
    synopsis = await get_movie_synopsis(movie_name)
    await ctx.send(f"Synopsis for {movie_name}:\n{synopsis}")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use !recommend, !rate, or !synopsis.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument. Please provide the necessary information.")
    else:
        print(f"An error occurred: {error}")

# Run the bot with your token
bot.run(TOKEN)