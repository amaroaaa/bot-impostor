import os
import discord
import random
from discord.ext import commands
from discord import app_commands

# ---------- INTENTS ----------
# Asegúrate de activar también los intents en el Portal de Discord:
# - SERVER MEMBERS INTENT
# - MESSAGE CONTENT INTENT (si lo necesitas)
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True  # Para leer contenido de mensajes si lo usas

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------- EVENTO ON_READY ----------
@bot.event
async def on_ready():
    print("==========")
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    print("Sincronizando slash commands...")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)} comandos.")
    except Exception as e:
        print(f"Error sincronizando slash commands: {e}")
    print("==========")


# ---------- COMANDO /impostor ----------
@bot.tree.command(
    name="impostor",
    description="Inicia el juego del impostor con los jugadores mencionados."
)
async def impostor(interaction: discord.Interaction, jugadores: str):
    print(f"/impostor usado en {interaction.guild} por {interaction.user}")

    ids = jugadores.split()
    miembros = []

    for item in ids:
        if item.startswith("<@") and item.endswith(">"):
            id_num = int(item.replace("<@", "").replace(">", "").replace("!", ""))
            miembro = interaction.guild.get_member(id_num)
            if miembro:
                miembros.append(miembro)

    if len(miembros) < 3:
        await interaction.response.send_message(
            "Necesitas **mínimo 3 jugadores** para jugar.",
            ephemeral=True
        )
        return

    palabras = [
        "LÁPIZ", "CUADERNO", "MOCHILA", "MESA", "SILLA",
        "TELEVISOR", "CONTROL REMOTO", "CELULAR", "CARGADOR", "AUDÍFONOS",
        "TECLADO", "MOUSE", "MONITOR", "NOTEBOOK", "IMPRESORA",
        "BOTELLA", "VASO", "TERMO", "TARRO", "PLATO",
        "CUCHILLO", "TENEDOR", "CUCHARA", "SARTÉN", "OLLA",
        "ZAPATO", "POLERA", "PANTALÓN", "CHAQUETA", "GORRO",
        "LLAVE", "BILLETERA", "TARJETA", "RELOJ", "PULSERA",
        "CAMA", "ALMOHADA", "FRAZADA", "COLCHÓN", "VELADOR",
        "PUERTA", "VENTANA", "CORTINA", "ESPEJO", "LÁMPARA",
        "CEPILLO DE DIENTES", "PASTA DENTAL", "JABÓN", "TOALLA", "SHAMPOO"
    ]

    palabra_secreta = random.choice(palabras)
    impostor = random.choice(miembros)

    await interaction.response.send_message(
        "🎮 **¡El juego del Impostor comenzó!** Revisen sus mensajes privados.",
        ephemeral=False
    )

    for jugador in miembros:
        try:
            if jugador == impostor:
                await jugador.send("😈 **ERES EL IMPOSTOR.** Finge que sabes la palabra.")
            else:
                await jugador.send(f"🔐 Tu palabra secreta es: **{palabra_secreta}**")
        except:
            await interaction.channel.send(
                f"No pude enviar DM a {jugador.mention} porque tiene los mensajes privados desactivados."
            )


# ---------- MAIN ----------
def main():
    token = os.getenv("TOKEN")
    print("TOKEN encontrado en Railway?:", token is not None)
    if not token:
        raise RuntimeError(
            "No se encontró la variable de entorno TOKEN. "
            "Configúrala en Railway → Variables."
        )
    bot.run(token)


if __name__ == "__main__":
    main()
