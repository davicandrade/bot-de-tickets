# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 

import json
import os
import asyncio
import aiohttp
import discord

def _leitura_sincrona():
    try:
        with open("database.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _escrita_sincrona(db_data):
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(db_data, f, indent=4)

async def ler_db():
    if not os.path.exists("database.json"):
        return {}
    return await asyncio.to_thread(_leitura_sincrona)

async def salvar_db(db_data):
    await asyncio.to_thread(_escrita_sincrona, db_data)

class DiscordV2API:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        self.base_url = "https://discord.com/api/v10"

    async def _fazer_requisicao(self, method, url, data=None):
        kwargs = {}
        if data is not None:
            kwargs['data'] = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.headers, **kwargs) as resp:
                status = resp.status
                texto = await resp.text()
                if status not in (200, 201, 204):
                    print(f"[API V2] Erro {status} na URL {url}: {texto}")
                return status, texto

    async def defer(self, interaction: discord.Interaction, ephemeral: bool = False):
        url = f"{self.base_url}/interactions/{interaction.id}/{interaction.token}/callback"
        flags = 64 if ephemeral else 0
        await self._fazer_requisicao("POST", url, data={"type": 5, "data": {"flags": flags}})

    async def responder_interacao(self, interaction: discord.Interaction, tipo: int, data: dict = None):
        url = f"{self.base_url}/interactions/{interaction.id}/{interaction.token}/callback"
        payload = {"type": tipo}
        if data:
            payload["data"] = data
        await self._fazer_requisicao("POST", url, data=payload)

    async def editar_mensagem_original(self, interaction: discord.Interaction, data: dict):
        url = f"{self.base_url}/webhooks/{interaction.application_id}/{interaction.token}/messages/@original"
        await self._fazer_requisicao("PATCH", url, data=data)

    async def enviar_mensagem(self, channel_id: int, data: dict):
        url = f"{self.base_url}/channels/{channel_id}/messages"
        status, _ = await self._fazer_requisicao("POST", url, data=data)
        return status in (200, 201)
    
# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 