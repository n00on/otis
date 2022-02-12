import discord
from yahoo_fin import stock_info as si
from datetime import datetime
from datetime import timedelta
from random import randint

from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):

	content = message.content

	if message.author == client.user or len(content) <= 1:
		return
		
	
	if "skate" in content:
		await message.channel.send("Ist Skatepark trocken?")
		return

	# normal commands
	if content[0] == "-":
		await commands(message)
		return
	
	# stock commands
	if content[0] == "$":
		await message.channel.send(await stocks(content[1:]))
		return
		

""" Commands using prefix "-". """
async def commands(message):
	command = message.content[1:].split()
	
	match command[0]:
		case "hello":
			await message.channel.send("Hello!")
		case "help":
			await message.channel.send("Ya aint gettin no help.")
		case "rps":
			if len(command) > 1:
				await message.channel.send(await rps(command[1]))
			else:
				await message.channel.send(await rps())
		case "coin":
			if randint(0,1) == 0:
				await message.channel.send("||Heads.||:coin:")
			else:
				await message.channel.send("||Tails.||:coin:")
		case "pleb":
			role = get(message.guild.roles, name="Pleb")
			if role is not None:
				answer = str(await pleb(message.guild.members, role)) + " members promoted"
				await message.channel.send(answer)
		case "promote":
			user_id = int(command[1][3:len(command[1])-1])
			role = get(message.guild.roles, name=command[2])
			member = message.guild.get_member(user_id)
			# if role and member found
			if role is None or member is None:
				await message.channel.send("404: User or Role not found.")
				return
			# if authorized
			if message.author.top_role <= role:
				await message.channel.send("Unauthorized")
				return
			await member.add_roles(role)
			await message.channel.send("Promotion successfull!")

		
""" This promotes 1d members, who have no role yet."""
async def pleb(members, pleb) -> int:
	counter = 0
	for member in members:
		# if member has no roles and joined more than 1d ago
		if len(member.roles) <= 1 and datetime.now() - member.joined_at >= timedelta(days=1):
			counter += 1
			await member.add_roles(pleb)
	return counter

""" Rock, Paper & Scissors. """
async def rps(enemy: str="") -> str:
	enemy = enemy.lower()
	choice = randint(0,2)
	if choice == 0:
		answer = "||Stone: "
	elif choice == 1:
		answer = "||Paper: "
	else:
		answer = "||Scissors: "
	
	if enemy.startswith("st"):
		enemy = 0
	elif enemy.startswith("pa"):
		enemy = 1
	elif enemy.startswith("sc"):
		enemy = 2
	else:
		return answer + "Threat unknown.||"
	
	if choice == enemy:
		return answer + "Draw..||"
	elif choice == (enemy + 1) % 3:
		return answer + "You loose!:x:||"
	else:
		return answer + "You win..:sos:||"
	

""" Returns live stock price, if possible, using prefix "$"."""
async def stocks(stock: str) -> str:
	try:
		usd = si.get_live_price(stock)
		eur = usd / si.get_currencies().at[0, "Last Price"]
		answer = str(round(usd, 2)) + " USD\t\t" + str(round(eur, 2)) + " EUR"
		# AMC AND GME GO MOON
		if stock.lower() == "amc" or stock.lower() == "gme":
			answer += " :rocket::rocket:"
		return answer
	except (Exception, RuntimeWarning):
		return "Stock " + stock + " not found."
		
client.run(open("token.txt", 'r').read())