import discord
from discord.ext import commands, tasks
import asyncio

TOKEN = 'Сюда ваш токен'
PREFIX = '?'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    game = discord.Game("?com")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def infor(ctx):
    embed = discord.Embed(title="Информация о боте", description="Приватный бот для дискорд сервера ИксДалина", color=0x00ff00)
    embed.add_field(name="Создатель", value="thdekk", inline=False)
    embed.add_field(name="Идея от", value="x_tik_555, diaval_g", inline=False)
    embed.add_field(name="Сообщение об ошибках", value="Пишите: thedekk", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def rules(ctx):
    embed = discord.Embed(title="Правила игры", description="Как играть:", color=0x00ff00)
    embed.add_field(name="1. Отвечайте на вопросы самым развернутым ответом.", value="В каждой игре будет 5 раундов, в которых вам нужно будет ответить на вопросы.", inline=False)
    embed.add_field(name="2. Общие правила:", value="⊹Нельзя повторять слова, которые уже были использованы в других раундах.\n*Наказание: Убирается 5 букв из вашего следующего ответа.\n...\n⊹Запрещено использование поисковых систем.\n*Наказание: Ответ не будет засчитан.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def com(ctx):
    embed = discord.Embed(title="Список команд", description="?create_channel [название категории] [название канала] - Создаёт канал в категории\n?clear [количество] - Удаляет какое-то число сообщений. Если не указывать, удалит все!\n?rules - Показывает правила игры.\n?infor - Немного информации о боте!\n?set_role_name [Название роли] - Указать роль, которая будет выдаваться игрокам для игры.\n?go - Раздать роль для начала игры\n?delir - Забрать роль игры у всех игроков.\n?mes - Написать от имени бота.\n?com - Показывает команды.\n?finish [Пинг игрока] - Показывает сколько букв написал этот игрок в этом канале.\n?admin - Объяснение для администрации.", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(name='create_channel')
@commands.has_permissions(manage_channels=True)
async def create_channel(ctx, category_name, channel_name):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)
    
    if category:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if role:
            channel = await guild.create_text_channel(name=channel_name, category=category)
            await channel.set_permissions(role, read_messages=True, send_messages=True)
            
            embed = discord.Embed(title="Канал создан", description=f"Канал {channel_name} был создан в категории {category_name}. Только участники с ролью {role_name} могут писать в этот канал.", color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Ошибка", description=f"Роль {role_name} не найдена на сервере.", color=0xff0000)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Ошибка", description=f"Категория {category_name} не существует.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)
    await channel.delete_messages(messages)
    embed = discord.Embed(title="Удалено сообщений", description=f'{amount} сообщений было удалено.', color=0x00ff00)
    await ctx.send(embed=embed)

@clear.error
@commands.has_permissions(administrator=True)
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Ошибка", description="У вас нет разрешения на удаление сообщений в этом канале.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command()
async def mes(ctx, *, message):
    await ctx.message.delete()  # Удаляем сообщение пользователя
    embed = discord.Embed(title="Сообщение от бота", description=message, color=0x00ff00)
    await ctx.send(embed=embed)

# игра

@bot.command()
async def finish(ctx, *, pinged_member: discord.Member = None):
    if pinged_member is None:
        pinged_member = ctx.author

    channel = ctx.channel
    total_letters_count = 0
    
    async for message in channel.history(limit=None):
        if message.author == pinged_member:
            for char in message.content:
                if char.isalpha():
                    total_letters_count += 1

    embed = discord.Embed(title="Статистика", description=f"{pinged_member.mention} написал(а) общее количество букв: {total_letters_count}", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
async def admin(ctx):
    embed = discord.Embed(title="Инструкция для администрации", description='Больше спасибо что пользуетесь этим ботом! Сейчас мы расскажем как его настроить для игр. Сначала вам надо создать роль для игроков, после этого вам надо еë указать такой командой: ?set_role_name [Название роли] После этого вам надо создать канал  командой: ?create_channel [название категории] [название канала] проверьте чтобы там могли писать только те люди у которых есть роль игроков, вообще это уже должно быть прописано в коде, но лучше всë проверить. Теперь для старта пропишите: ?go и все люди которые будут участвовать нужно нажать на эмодзи и им будет выдана роль. После того как все игроки получили роль вы можете начать играть, чтобы начать задавать вопросы пропишите: ?mes и ваш вопрос. (К сожалению пока нет автоматической системы но мы будем работать над ней!) После конца игры вы должны забрать роль игроков командой: ?delir и теперь вы можете посчитать буквы игроков командой: ?finish [Пинг игрока]. А чтобы отчистить чат пропишите команду: ?clear', color=0x00ff00)
    await ctx.send(embed=embed)

# роль
@bot.command(name='set_role_name')
@commands.has_permissions(administrator=True)
async def set_role_name(ctx, new_role_name):
    global role_name
    role_name = new_role_name
    embed = discord.Embed(title="Установка роли", description=f"Значение переменной `role_name` установлено на: {new_role_name}", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)  # Поменяйте manage_roles на нужное разрешение
async def go(ctx, number_of_people: int = 100000):
    emoji = '👍'  # Замените на вашу эмодзи
    message = await ctx.send(f"Нажмите на реакцию {emoji} чтобы получить роль {role_name}")
    await message.add_reaction(emoji)

    def check(reaction, user):
        return str(reaction.emoji) == emoji and user != bot.user

    try:
        reactions, users = await bot.wait_for('reaction_add', timeout=60.0, check=check, count=number_of_people)
    except asyncio.TimeoutError:
        embed = discord.Embed(title="Время вышло", description="Никто не нажал на реакцию.", color=0xff0000)
        await ctx.send(embed=embed)
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        for user in users:
            await user.add_roles(role)
        embed = discord.Embed(title="Роль выдана", description=f"Роль {role_name} была выдана {', '.join([user.mention for user in users])}", color=0x00ff00)
        await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await message.delete()
    else:
        embed = discord.Embed(title="Ошибка", description=f"Роль {role_name} не найдена на сервере.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(name='delir')
@commands.has_permissions(manage_roles=True)  # Поменяйте manage_roles на нужное разрешение
async def remove_role_from_all(ctx):
    role = discord.utils.get(ctx.guild.roles, name=role_name)

    if role:
        for member in ctx.guild.members:
            if role in member.roles:
                await member.remove_roles(role)

        embed = discord.Embed(title="Роль удалена", description=f"Роль {role_name} была удалена у всех участников сервера.", color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Ошибка", description=f"Роль {role_name} не найдена на сервере.", color=0xff0000)
        await ctx.send(embed=embed)

role_name = ''

bot.run(TOKEN)
