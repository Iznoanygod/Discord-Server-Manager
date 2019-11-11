import discord
import psutil
import asyncio

class Bot(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        client.loop.create_task(client.status_task())

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        if message.content == '!ping':
            await message.channel.send('pong')
        if message.content == '!logo':
            await message.channel.send(file=discord.File('bot.png'))
        if message.content == '!usage':
            mess = '```'
            uss = psutil.cpu_percent(percpu=True)
            ram = psutil.virtual_memory()
            for x in range(0, psutil.cpu_count()):
               mess =  mess + (str(x + 1) + '  ')[:3] + '[' + usage_to_bar(uss[x]) + '] ' + str(uss[x]) + '%\n'
            mess = mess + 'Mem[' + ram_usage(ram.used,ram.total) + '] ' + byte_to_largest(ram.used) + '/' + byte_to_largest(ram.total) + '\n'
            await message.channel.send(mess + '```')
            await message.channel.send(psutil.disk_usage('/'))
            await message.channel.send(psutil.net_io_counters(pernic=True))

    async def status_task(self):
        while True:
            use = psutil.cpu_percent()
            if use < 50:
                status = discord.Status.online
            elif use < 75:
                status = discord.Status.idle
            else:
                status = discord.Status.dnd
            activity = discord.Activity(name='cpu usage at ' + str(use) + '%',type=discord.ActivityType.watching)
            await client.change_presence(status=status,activity=activity)
            await asyncio.sleep(5)

def usage_to_bar(usage):
    usage = usage / 5
    tt = ''
    for x in range(0, round(usage)):
        tt = tt + '|'
    for x in range(round(usage), 20):
        tt = tt + ' '
    return tt
def ram_usage(used,max):
    usage = used * 20 / max
    tt = ''
    for x in range(0, round(usage)):
        tt = tt + '|'
    for x in range(round(usage), 20):
        tt = tt + ' '
    return tt
def byte_to_largest(value):
    x = value
    y = 0
    prefix = ['B','K','M','G','T','P']
    while True:
        if x / 1024 > 1:
            x = x / 1024
            y += 1
        else:
            break
    return str(round(x,2)) + prefix[y]

client = Bot()
client.run('')
