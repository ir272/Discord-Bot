import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

ian_role = "Ian"

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents) 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print("Commands:", [c.name for c in client.commands])

# welcomes new members to the server in #general
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')

# prevents infinite loop by ignoring messages from itself
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # replies with apple emoji if bot detects "apple" in a users message
    if "apple" in message.content.lower():
        await message.channel.send("🍎")
    # if bot detects "banana" in users message, it deletes the message and follows up
    if "banana" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, bananas are not allowed here!")

    await client.process_commands(message)

# !hello command
@client.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!') 

# !ping command
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

# !echo command
@client.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

# !add command
@client.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b) 

@client.command()
async def assign(ctx, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f'Role `{role_name}` does not exist.')
        return

    await ctx.author.add_roles(role)
    await ctx.send(f'{ctx.author.mention} now has {role.name}.')

@client.command()
async def remove(ctx, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role is None:
        await ctx.send(f'Role `{role_name}` does not exist.')
        return

    await ctx.author.remove_roles(role)
    await ctx.send(f'{ctx.author.mention} no longer has {role.name}.')

@client.command()
@commands.has_role(ian_role)
async def secret(ctx):
    await ctx.send('We love you Ian')

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You don't have the required role to use this command.")

client.run(token, log_handler=handler, log_level=logging.DEBUG)