# 🎫 Discord Bot de Ticket`s — Discord V2 Components

Um sistema de tickets moderno para Discord, utilizando os novos **Components V2** para uma interface visual mais bonita. Este bot foi projetado para comunidades que buscam um atendimento organizado, rápido e esteticamente agradável.

## 🛠️ Como Obter o Token do Bot

Para colocar o bot online, você precisará de um token do **Discord Developer Portal**:

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).

2. Clique em **"New Application"** e dê um nome ao seu bot.

3. No menu lateral esquerdo, vá em **"Bot"**.

4. Clique em **"Reset Token"** (ou "Copy Token") para gerar o seu token. **Guarde-o bem!**

5. Role para baixo até a seção **"Privileged Gateway Intents"** e ative:
  - `Presence Intent`
  - `Server Members Intent`
  - `Message Content Intent` (Obrigatório para o bot ler comandos).

6. No seu computador, abra o arquivo `.env-exemplo` e cole o token:

   ```
   DISCORD_TOKEN=COLE_SEU_TOKEN_AQUI
   ```
7. Renomeie o arquivo `.env-exemplo` para `.env`

## ⚙️ Comando de Configuração: `/configurar`

O sistema é totalmente dinâmico. Após convidar o bot para o seu servidor, use o comando slash `/configurar` para abrir o painel de controle (apenas os usuários com permissão de administrador podem utilizá-lo).

### Opções Disponíveis:

- **Painel de Atendimento:** Define em qual canal a mensagem de "Abrir Ticket" será enviada.

- **Categoria de Tickets:** Define em qual categoria os novos canais de atendimento serão criados.

- **Canal de Logs/Relatórios:** Define onde os relatórios de encerramento (quem abriu, quem fechou, etc.) serão enviados.

- **Cargos de Suporte:** Define quais cargos têm permissão para visualizar e fechar os tickets.

- **Considerações Finais:** Ative ou desative a obrigatoriedade de preencher um motivo ao fechar o ticket.

## ✨ Diferenciais Visuais

Diferente da maioria dos bots que utilizam apenas embeds padrão, este sistema utiliza a **API V10 do Discord** para renderizar:

- **Layouts Complexos:** Uso de grids e divisores avançados.

- **Micro-interações:** Respostas rápidas e modais de fechamento com relatórios detalhados.

## 🚀 Instalação Rápida

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/bot-de-tickets.git
   cd bot-de-tickets
   ```

1. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

1. **Inicie o bot:**

   ```bash
   python main.py
   ```

## 📁 Estrutura do Projeto

```
├── cogs/
│   ├── config.py    # Comandos de configuração (/configurar )
│   └── ticket.py    # Lógica principal de atendimento
├── main.py          # Ponto de entrada
├── utils.py         # Funções auxiliares e API V10
├── database.json    # Banco de dados leve (gerado automaticamente)
├── requirements.txt # Dependências do bot
└── .env             # Token do bot
```

## 👤 Créditos

Desenvolvido por [**Davi Andrade**](https://github.com/davicandrade).
*Este projeto é open-source e focado na evolução da UI/UX para Discord.*
> **Nota:** Este bot utiliza recursos avançados. Certifique-se de que o bot tenha permissão de `Administrator` no servidor.
