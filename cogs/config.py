# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 

import discord
from discord import app_commands
from discord.ext import commands
from utils import ler_db, salvar_db, DiscordV2API

COMPONENTS_V2_DO_DISCORD = 1 << 15
EPHEMERAL_DISCORD = 1 << 6
LOGO_DISCORD = "https://i.postimg.cc/wBwSrsWT/image.png"


def build_overview_payload(guild, db_data):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD

    canal_atual = f"<#{db_data['canal_id']}>" if db_data and db_data.get('canal_id') else "Não definido"
    categoria_atual = f"<#{db_data['categoria_id']}>" if db_data and db_data.get('categoria_id') else "Não definida"
    cargos_atuais = ", ".join([f"<@&{c}>" for c in db_data.get('cargos_suporte', [])]) if db_data and db_data.get('cargos_suporte') else "Não definidos"

    canal_relatorio_atual = f"<#{db_data['canal_relatorio_id']}>" if db_data and db_data.get('canal_relatorio_id') else "Não definido"
    consideracoes_atual = "Ativadas ✅" if (db_data and db_data.get('consideracoes_finais_habilitado')) else "Desativadas ❌"

    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# 📋 Painel de Configuração\n-# Visão geral do sistema de tickets"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 9,
            "components": [{
                "type": 10,
                "content": (
                    f"**🎫 Painel de Ticket**\n"
                    f"> **Canal:** {canal_atual}\n"
                    f"> **Categoria:** {categoria_atual}\n"
                    f"> **Cargos:** {cargos_atuais}"
                )
            }],
            "accessory": {"type": 2, "style": 1, "label": "Configurar", "custom_id": "cfg_ir_painel", "emoji": {"name": "⚙️"}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 9,
            "components": [{
                "type": 10,
                "content": (
                    f"**🛠️ Configurações Avançadas**\n"
                    f"> **Canal de Relatório:** {canal_relatorio_atual}\n"
                    f"> **Considerações Finais:** {consideracoes_atual}"
                )
            }],
            "accessory": {"type": 2, "style": 2, "label": "Configurar", "custom_id": "cfg_avancado", "emoji": {"name": "🛠️"}}
        },
        {"type": 14, "divider": True, "spacing": 2},
        {"type": 10, "content": f"-# {guild.name} • Central de Configuração"}
    ]

    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": components_v2}]
    }

def build_config_payload(guild, session, db_data):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD

    if session.get('saved'):
        return {
            "flags": COMPONENTS_V2_DO_DISCORD,
            "components": [{
                "type": 17,
                "accent_color": 0x57F287,
                "components": [
                    {
                        "type": 9,
                        "components": [{"type": 10, "content": "# ✅ Configuração Concluída\n-# Sistema de tickets configurado com sucesso"}],
                        "accessory": {"type": 11, "media": {"url": icon_url}}
                    },
                    {"type": 14, "divider": True, "spacing": 1},
                    {
                        "type": 10,
                        "content": (
                            f"> **Painel Enviado:** <#{session['canal_id']}>\n"
                            f"> **Categoria Destino:** <#{session['categoria_id']}>\n"
                            f"> **Cargos de Suporte:** " + ", ".join([f"<@&{c}>" for c in session['cargos_suporte']]) + "\n\n"
                            f"O painel de atendimento já está disponível no canal selecionado e pronto para uso."
                        )
                    },
                    {"type": 14, "divider": True, "spacing": 2},
                    {
                        "type": 1,
                        "components": [{"type": 2, "style": 2, "label": "Voltar ao Menu", "custom_id": "cfg_voltar", "emoji": {"name": "↩️"}}]
                    },
                    {"type": 14, "divider": True, "spacing": 2},
                    {"type": 10, "content": f"-# {guild.name} • Central de Configuração"}
                ]
            }]
        }

    canal_atual = f"<#{db_data['canal_id']}>" if db_data and db_data.get('canal_id') else "Inválido"
    categoria_atual = f"<#{db_data['categoria_id']}>" if db_data and db_data.get('categoria_id') else "Inválida"
    cargos_atuais = ", ".join([f"<@&{c}>" for c in db_data.get('cargos_suporte', [])]) if db_data and db_data.get('cargos_suporte') else "Inválidos"

    canal_str = f"<#{session['canal_id']}>" if session.get('canal_id') else "Pendente"
    categoria_str = f"<#{session['categoria_id']}>" if session.get('categoria_id') else "Pendente"
    cargos_str = ", ".join([f"<@&{c}>" for c in session.get('cargos_suporte', [])]) if session.get('cargos_suporte') else "Pendente"

    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# ⚙️ Painel de Configuração\n-# Ajuste os parâmetros de tickets do servidor"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 10,
            "content": (
                f"**📌 Configuração Atual**\n"
                f"> **Canal:** {canal_atual}\n"
                f"> **Categoria:** {categoria_atual}\n"
                f"> **Cargos:** {cargos_atuais}"
            )
        },
        {"type": 14, "divider": True, "spacing": 2},
        {"type": 10, "content": f"**1️⃣ Canal do Painel** — {canal_str}"},
        {
            "type": 1,
            "components": [{"type": 8, "custom_id": "cfg_canal", "placeholder": "Selecione o canal do painel", "channel_types": [0]}]
        },
        {"type": 10, "content": f"**2️⃣ Categoria dos Tickets** — {categoria_str}"},
        {
            "type": 1,
            "components": [{"type": 8, "custom_id": "cfg_categoria", "placeholder": "Selecione a categoria dos tickets", "channel_types": [4]}]
        },
        {"type": 10, "content": f"**3️⃣ Cargos de Suporte** — {cargos_str}"},
        {
            "type": 1,
            "components": [{"type": 6, "custom_id": "cfg_cargos", "placeholder": "Selecione os cargos de suporte", "min_values": 1, "max_values": 5}]
        },
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [
                {"type": 2, "style": 3, "label": "Salvar e Enviar Painel", "custom_id": "cfg_salvar", "emoji": {"name": "💾"}},
                {"type": 2, "style": 2, "label": "Voltar", "custom_id": "cfg_voltar", "emoji": {"name": "↩️"}}
            ]
        }
    ]

    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": components_v2}]
    }

def build_current_config_info_payload(guild, db_data):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD

    canal_atual = f"<#{db_data['canal_id']}>" if db_data.get('canal_id') else "Não definido"
    categoria_atual = f"<#{db_data['categoria_id']}>" if db_data.get('categoria_id') else "Não definida"
    cargos_atuais = ", ".join([f"<@&{c}>" for c in db_data.get('cargos_suporte', [])]) if db_data.get('cargos_suporte') else "Não definidos"

    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# ⚙️ Configuração Já Existente\n-# Este servidor já possui um sistema de tickets configurado"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 10,
            "content": (
                f"**📌 Configuração Vigente**\n"
                f"> **Canal do Painel:** {canal_atual}\n"
                f"> **Categoria dos Tickets:** {categoria_atual}\n"
                f"> **Cargos de Suporte:** {cargos_atuais}\n\n"
                f"Você pode prosseguir para revisar e alterar essas configurações."
            )
        },
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [
                {"type": 2, "style": 1, "label": "Prosseguir", "custom_id": "cfg_prosseguir", "emoji": {"name": "➡️"}},
                {"type": 2, "style": 2, "label": "Voltar", "custom_id": "cfg_voltar", "emoji": {"name": "↩️"}}
            ]
        }
    ]

    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": components_v2}]
    }

def build_advanced_config_payload(guild, session, db_data):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD

    canal_relatorio_atual = f"<#{db_data['canal_relatorio_id']}>" if db_data and db_data.get('canal_relatorio_id') else "Não definido"
    canal_relatorio_str = f"<#{session['canal_relatorio_id']}>" if session.get('canal_relatorio_id') else "Pendente"

    consideracoes_novo = session.get('consideracoes_finais_habilitado')
    if consideracoes_novo is None:
        consideracoes_novo = bool(db_data.get('consideracoes_finais_habilitado')) if db_data else False

    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# 🛠️ Configurações Avançadas\n-# Relatório de tickets e considerações finais"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {"type": 10, "content": f"**📨 Canal de Relatório** — Atual: {canal_relatorio_atual} • Novo: {canal_relatorio_str}"},
        {
            "type": 1,
            "components": [{"type": 8, "custom_id": "cfg_canal_relatorio", "placeholder": "Selecione o canal de relatório", "channel_types": [0]}]
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 10,
            "content": (
                "**📝 Considerações Finais**\n"
                "-# Ao ativar, um formulário pedindo as considerações finais do atendimento será exibido ao fechar um ticket, e o texto será anexado ao relatório."
            )
        },
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 3 if consideracoes_novo else 2,
                    "label": "Ativado" if consideracoes_novo else "Ativar",
                    "custom_id": "cfg_consideracoes_ativar",
                    "emoji": {"name": "☑️" if consideracoes_novo else "⬜"},
                    "disabled": consideracoes_novo
                },
                {
                    "type": 2,
                    "style": 4 if not consideracoes_novo else 2,
                    "label": "Desativado" if not consideracoes_novo else "Desativar",
                    "custom_id": "cfg_consideracoes_desativar",
                    "emoji": {"name": "☑️" if not consideracoes_novo else "⬜"},
                    "disabled": not consideracoes_novo
                }
            ]
        },
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [
                {"type": 2, "style": 3, "label": "Salvar", "custom_id": "cfg_salvar_avancado", "emoji": {"name": "💾"}},
                {"type": 2, "style": 2, "label": "Voltar", "custom_id": "cfg_voltar", "emoji": {"name": "↩️"}}
            ]
        }
    ]

    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x2b2d31, "components": components_v2}]
    }

def build_ticket_panel_payload(guild):
    icon_url = str(guild.icon.url) if guild.icon else LOGO_DISCORD
    components_v2 = [
        {
            "type": 9,
            "components": [{"type": 10, "content": "# ᯓ★ Central de Atendimento\n-# Atendimento seguro e privado"}],
            "accessory": {"type": 11, "media": {"url": icon_url}}
        },
        {"type": 14, "divider": True, "spacing": 1},
        {
            "type": 10,
            "content": "Precisa de ajuda? Clique no botão abaixo para abrir um ticket reservado.\nNossa equipe de suporte estará pronta para te ajudar o mais rápido possível."
        },
        {"type": 14, "divider": True, "spacing": 2},
        {
            "type": 1,
            "components": [{"type": 2, "style": 1, "label": "Solicitar Atendimento", "custom_id": "abrir_ticket", "emoji": {"name": "🎫"}}]
        }
    ]
    return {
        "flags": COMPONENTS_V2_DO_DISCORD,
        "components": [{"type": 17, "accent_color": 0x5865F2, "components": components_v2}]
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
                    "components": [{"type": 10, "content": "# ⚠️ Ação Interrompida\n-# Erro de verificação"}],
                    "accessory": {"type": 11, "media": {"url": icon_url}}
                },
                {"type": 14, "divider": True, "spacing": 1},
                {"type": 10, "content": f"> {message}"}
            ]
        }]
    }

class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}
        self.api = DiscordV2API(bot.http.token)

    def _nova_sessao(self):
        return {
            "canal_id": None,
            "categoria_id": None,
            "cargos_suporte": [],
            "confirmed": False,
            "canal_relatorio_id": None,
            "consideracoes_finais_habilitado": None,
            "saved": False
        }

    @app_commands.command(name="configurar", description="Interface interativa de configuração em v2.")
    @app_commands.default_permissions(administrator=True)
    async def configurar(self, interaction: discord.Interaction):
        await self.api.defer(interaction, EPHEMERAL_DISCORD =True)

        db = await ler_db()
        db_data = db.get(str(interaction.guild.id))

        self.sessions[interaction.user.id] = self._nova_sessao()
        payload = build_overview_payload(interaction.guild, db_data)

        await self.api.editar_mensagem_original(interaction, payload)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id")
        acoes_conhecidas = {
            "cfg_ir_painel", "cfg_canal", "cfg_categoria", "cfg_cargos", "cfg_salvar",
            "cfg_prosseguir", "cfg_avancado", "cfg_canal_relatorio", "cfg_consideracoes_ativar",
            "cfg_consideracoes_desativar", "cfg_salvar_avancado", "cfg_voltar"
        }

        if custom_id not in acoes_conhecidas:
            return

        user_id = interaction.user.id
        session = self.sessions.setdefault(user_id, self._nova_sessao())

        db = await ler_db()
        guild_id = str(interaction.guild.id)
        db_data = db.get(guild_id)

        if custom_id == "cfg_voltar":
            self.sessions[user_id] = self._nova_sessao()
            payload = build_overview_payload(interaction.guild, db_data)
            await self.api.responder_interacao(interaction, 7, payload)
            return

        elif custom_id == "cfg_ir_painel":
            tem_config = bool(db_data and db_data.get("canal_id") and db_data.get("categoria_id") and db_data.get("cargos_suporte"))
            if tem_config and not session.get("confirmed"):
                payload = build_current_config_info_payload(interaction.guild, db_data)
            else:
                session["confirmed"] = True
                payload = build_config_payload(interaction.guild, session, db_data)
            await self.api.responder_interacao(interaction, 7, payload)
            return

        elif custom_id == "cfg_canal":
            session["canal_id"] = interaction.data["values"][0]
            await self.api.responder_interacao(interaction, 7, build_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_categoria":
            session["categoria_id"] = interaction.data["values"][0]
            await self.api.responder_interacao(interaction, 7, build_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_cargos":
            session["cargos_suporte"] = interaction.data["values"]
            await self.api.responder_interacao(interaction, 7, build_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_prosseguir":
            session["confirmed"] = True
            await self.api.responder_interacao(interaction, 7, build_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_salvar":
            if not all([session.get("canal_id"), session.get("categoria_id"), session.get("cargos_suporte")]):
                err_payload = build_error_payload(interaction.guild, "Preencha todas as opções antes de salvar.")
                err_payload["flags"] = err_payload.get("flags", 0) | EPHEMERAL_DISCORD 
                await self.api.responder_interacao(interaction, 4, err_payload)
                return

            db.setdefault(guild_id, {})
            db[guild_id].update({
                "canal_id": session["canal_id"],
                "categoria_id": session["categoria_id"],
                "cargos_suporte": session["cargos_suporte"]
            })
            await salvar_db(db)

            sucesso = await self.api.enviar_mensagem(session["canal_id"], build_ticket_panel_payload(interaction.guild))
            
            if sucesso:
                session["saved"] = True
                await self.api.responder_interacao(interaction, 7, build_config_payload(interaction.guild, session, db_data))
            else:
                err_payload = build_error_payload(interaction.guild, "Falha ao enviar o painel. Verifique permissões.")
                err_payload["flags"] = err_payload.get("flags", 0) | EPHEMERAL_DISCORD 
                await self.api.responder_interacao(interaction, 4, err_payload)
            return

        elif custom_id == "cfg_avancado":
            if session.get("consideracoes_finais_habilitado") is None:
                session["consideracoes_finais_habilitado"] = bool(db_data.get("consideracoes_finais_habilitado")) if db_data else False
            await self.api.responder_interacao(interaction, 7, build_advanced_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_canal_relatorio":
            session["canal_relatorio_id"] = interaction.data["values"][0]
            await self.api.responder_interacao(interaction, 7, build_advanced_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id in ("cfg_consideracoes_ativar", "cfg_consideracoes_desativar"):
            session["consideracoes_finais_habilitado"] = (custom_id == "cfg_consideracoes_ativar")
            await self.api.responder_interacao(interaction, 7, build_advanced_config_payload(interaction.guild, session, db_data))
            return

        elif custom_id == "cfg_salvar_avancado":
            db.setdefault(guild_id, {})
            db[guild_id]["canal_relatorio_id"] = session.get("canal_relatorio_id") or (db_data.get("canal_relatorio_id") if db_data else None)
            
            cons_final = session.get("consideracoes_finais_habilitado")
            db[guild_id]["consideracoes_finais_habilitado"] = cons_final if cons_final is not None else (bool(db_data.get("consideracoes_finais_habilitado")) if db_data else False)
            
            await salvar_db(db)
            await self.api.responder_interacao(interaction, 7, build_advanced_config_payload(interaction.guild, session, db[guild_id]))
            return

async def setup(bot):
    await bot.add_cog(ConfigCog(bot))

# Por davicandrade
# Baixe mais códigos em https://github.com/davicandrade 