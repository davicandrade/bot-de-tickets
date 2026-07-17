# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 

import discord
from discord.ext import commands
from utils import ler_db, salvar_db, DiscordV2API
import time

COMPONENTS_V2_DO_DISCORD = 1 << 15
EPHEMERAL_DISCORD = 1 << 6
LOGO_DISCORD = "https://i.postimg.cc/wBwSrsWT/image.png"

def build_ticket_created_payload(guild, user, mencoes_equipe):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD
    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": f"# 🎫 Central de Suporte\n-# Ticket de Atendimento • {guild.name}"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 10,
            "content": (
                f"Olá {user.mention},\n\n"
                f"A equipe responsável foi notificada e logo iniciará o seu atendimento.\n"
                f"Por favor, descreva detalhadamente sua solicitação e envie provas caso seja necessário para agilizar o suporte.\n\n"
                f"> **Equipe notificada:** {mencoes_equipe}"
            )
        },
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [{"type": 2, "style": 4, "label": "Encerrar Ticket", "custom_id": "fechar_ticket_suporte", "emoji": {"name": "🔒"}}]
        }
    ]
    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": components_v2}]
    }

def build_ticket_success_payload(guild, channel_id):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD
    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# ✅ Ticket Aberto\n-# Atendimento Solicitado"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {"type": 10, "content": f"> O seu canal de atendimento privado foi criado com sucesso."},
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [{"type": 2, "style": 5, "label": "Ir para o Ticket", "url": f"https://discord.com/channels/{guild.id}/{channel_id}", "emoji": {"name": "🔗"}}]
        }
    ]
    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x57F287, "components": components_v2}]
    }

def build_error_payload(guild, message):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD
    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{
            "type": 17,
            "accent_color": 0xED4245,
            "components": [
                {
                    "type": 9,
                    "components": [{"type": 10, "content": "# ⚠️ Operação Interrompida\n-# Sistema de Tickets"}],
                    "accessory": {"type": 11, "media": {"url": icon_url}}
                },
                {"type": 14, "divider": True, "spacing": 1},
                {"type": 10, "content": f"> {message}"}
            ]
        }]
    }

def build_ticket_report_payload(guild, canal_nome, aberto_por_id, fechado_por_id, aberto_em_unix, fechado_em_unix, consideracoes_finais=None):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD

    aberto_por_str = f"<@{aberto_por_id}> | `{aberto_por_id}`" if aberto_por_id else "Desconhecido"
    fechado_por_str = f"<@{fechado_por_id}> | `{fechado_por_id}`" if fechado_por_id else "Desconhecido"
    aberto_em_str = f"<t:{aberto_em_unix}:F>" if aberto_em_unix else "Desconhecido"
    fechado_em_str = f"<t:{fechado_em_unix}:F>" if fechado_em_unix else "Desconhecido"

    conteudo = (
        f"> **Ticket:** #{canal_nome}\n"
        f"> **Aberto por:** {aberto_por_str}\n"
        f"> **Fechado por:** {fechado_por_str}\n"
        f"> **Aberto em:** {aberto_em_str}\n"
        f"> **Fechado em:** {fechado_em_str}"
    )

    componentes = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# 📄 Relatório de Ticket\n-# Registro de encerramento de atendimento"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {"type": 10, "content": conteudo}
    ]

    if consideracoes_finais:
        componentes.append({"type": 14, "divider": True, "spacing": 1})
        componentes.append({"type": 10, "content": f"**📝 Considerações Finais**\n> {consideracoes_finais}"})

    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": componentes}]
    }

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = DiscordV2API(bot.http.token)

    async def _gerar_e_enviar_relatorio(self, guild, channel_id, channel_name, fechado_por_id, consideracoes_finais=None):
        db = await ler_db()
        guild_id = str(guild.id)
        
        ticket_info = db.get(guild_id, {}).get("tickets", {}).get(str(channel_id), {})
        aberto_por_id = ticket_info.get("usuario_id")
        aberto_em_unix = ticket_info.get("aberto_em_unix")
        fechado_em_unix = int(time.time())

        canal_relatorio_id = db.get(guild_id, {}).get("canal_relatorio_id")

        if canal_relatorio_id:
            payload_relatorio = build_ticket_report_payload(
                guild, channel_name, aberto_por_id, fechado_por_id,
                aberto_em_unix, fechado_em_unix, consideracoes_finais
            )
            await self.api.enviar_mensagem(canal_relatorio_id, payload_relatorio)

        # Limpa o ticket do DB
        if guild_id in db and "tickets" in db[guild_id]:
            db[guild_id]["tickets"].pop(str(channel_id), None)
            await salvar_db(db)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.modal_submit:
            if interaction.data.get("custom_id") == "modal_fechar_ticket":
                consideracoes = interaction.data.get("components", [])[0].get("components", [])[0].get("value")
                
                await self.api.responder_interacao(interaction, 6)

                channel_nome = interaction.channel.name if interaction.channel else str(interaction.channel_id)
                await self._gerar_e_enviar_relatorio(interaction.guild, interaction.channel_id, channel_nome, interaction.user.id, consideracoes)

                try:
                    await interaction.channel.delete(reason=f"Ticket fechado por {interaction.user.display_name}")
                except discord.Forbidden:
                    pass
            return

        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id")

        if custom_id == "fechar_ticket_suporte":
            db = await ler_db()
            guild_id = str(interaction.guild.id)
            db_data = db.get(guild_id, {})

            cargos = db_data.get("cargos_suporte", [])
            tem_permissao = interaction.user.guild_permissions.administrator or any(str(role.id) in cargos for role in interaction.user.roles)

            if not tem_permissao:
                err_payload = build_error_payload(interaction.guild, "Apenas a equipe de suporte pode fechar o ticket.")
                err_payload["flags"] = err_payload.get("flags", 0) | EPHEMERAL_DISCORD
                return await self.api.responder_interacao(interaction, 4, err_payload)

            if db_data.get("consideracoes_finais_habilitado"):
                modal_payload = {
                    "custom_id": "modal_fechar_ticket",
                    "title": "Encerrar Ticket",
                    "components": [{
                        "type": 1,
                        "components": [{
                            "type": 4,
                            "custom_id": "consideracoes_finais_input",
                            "style": 2,
                            "label": "Considerações finais",
                            "placeholder": "Como o atendimento foi concluído?",
                            "required": True,
                            "max_length": 1000
                        }]
                    }]
                }
                return await self.api.responder_interacao(interaction, 9, modal_payload)

            await self.api.responder_interacao(interaction, 6)
            channel_nome = interaction.channel.name if interaction.channel else str(interaction.channel_id)
            
            await self._gerar_e_enviar_relatorio(interaction.guild, interaction.channel_id, channel_nome, interaction.user.id)
            try:
                await interaction.channel.delete(reason=f"Ticket fechado por {interaction.user.display_name}")
            except discord.Forbidden:
                pass
            return

        if custom_id == "abrir_ticket":
            await self.api.defer(interaction, EPHEMERAL_DISCORD=True)
            db = await ler_db()
            guild_id = str(interaction.guild.id)

            if guild_id not in db or "categoria_id" not in db[guild_id]:
                return await self.api.editar_mensagem_original(interaction, build_error_payload(interaction.guild, "O sistema não está configurado."))

            categoria = interaction.guild.get_channel(int(db[guild_id]["categoria_id"]))
            if not categoria:
                return await self.api.editar_mensagem_original(interaction, build_error_payload(interaction.guild, "A categoria configurada não existe."))

            cargos_suporte = db[guild_id].get("cargos_suporte", [])
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)
            }

            for cargo_id in cargos_suporte:
                cargo = interaction.guild.get_role(int(cargo_id))
                if cargo:
                    overwrites[cargo] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

            try:
                canal_ticket = await interaction.guild.create_text_channel(
                    name=f"ticket-{interaction.user.name}",
                    category=categoria,
                    overwrites=overwrites
                )

                db.setdefault(guild_id, {})
                db[guild_id].setdefault("tickets", {})
                db[guild_id]["tickets"][str(canal_ticket.id)] = {
                    "usuario_id": str(interaction.user.id),
                    "aberto_em_unix": int(time.time())
                }
                await salvar_db(db)

                await self.api.editar_mensagem_original(interaction, build_ticket_success_payload(interaction.guild, canal_ticket.id))

                mencoes_equipe = " ".join([f"<@&{c_id}>" for c_id in cargos_suporte])
                await self.api.enviar_mensagem(canal_ticket.id, build_ticket_created_payload(interaction.guild, interaction.user, mencoes_equipe))

            except discord.Forbidden:
                await self.api.editar_mensagem_original(interaction, build_error_payload(interaction.guild, "Permissões insuficientes para criar canais."))

async def setup(bot):
    await bot.add_cog(TicketCog(bot))

# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 