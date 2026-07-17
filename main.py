# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class TicketBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"[OK] Cog carregada: {filename}")
                except Exception as e:
                    print(f"[ERRO] Falha ao carregar {filename}: {e}")
        
        await self.tree.sync()
        print("[OK] Comandos Slash sincronizados.")

    async def on_ready(self):
        print(f'Bot online! Logado como {self.user} (ID: {self.user.id})')

bot = TicketBot()

if __name__ == '__main__':
    if not TOKEN:
        print("Erro: DISCORD_TOKEN não encontrado no .env")
    else:
        bot.run(TOKEN)

# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 