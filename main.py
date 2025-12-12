import os
import discord
import random
from discord.ext import commands
from discord import app_commands
from keep_alive import keep_alive  # para que Replit mantenga el bot vivo

TOKEN = os.environ["TOKEN"]  # token seguro desde Secrets

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        await bot.tree.sync()
        print("Slash commands sincronizados correctamente.")
    except Exception as e:
        print(f"Error sincronizando slash commands: {e}")


# ================================
# COMANDO /impostor
# ================================
@bot.tree.command(name="impostor", description="Inicia el juego del impostor con los jugadores mencionados.")
async def impostor(interaction: discord.Interaction, jugadores: str):

    ids = jugadores.split()
    miembros = []

    # Convierte las menciones en IDs → luego en miembros
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


# Mantiene vivo el servidor web de Replit
keep_alive()

# Ejecuta el bot
bot.run(TOKEN)
