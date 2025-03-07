import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import ia_def
 
# Cargar variables de entorno
load_dotenv()
token = os.getenv("dt")
 
# Configurar intents y bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="&", intents=intents)
 
@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')
 
@bot.command(name="file")
async def save_file(ctx):
    if not ctx.message.attachments:
        await ctx.send("Olvidaste subir una imagen.")
        return
 
    attach = ctx.message.attachments[0]  # Tomar solo el primer archivo adjunto
    file_name = attach.filename
    await attach.save(f"./{file_name}")
    await ctx.send(f"Imagen guardada en `./{file_name}`.")
 
@bot.command(name="IA")
async def classify_image(ctx):
    if not ctx.message.attachments:
        await ctx.send("Olvidaste subir un archivo.")
        return
 
    attach = ctx.message.attachments[0]  # Tomar solo el primer archivo adjunto
    img_path = f"./{attach.filename}"
 
    # Guardar la imagen
    await attach.save(img_path)
 
    # Clasificar la imagen
    model_path = "./keras_model.h5"
    label_path = "./labels.txt"
    resultado = ia_def.classify_img(image_path=img_path, model_path=model_path, labels_path=label_path)
 
    # Validar resultado
    if not isinstance(resultado, (list, tuple)) or len(resultado) < 2:
        await ctx.send("Error al procesar la imagen.")
        return
 
    class_name, confidence_score = resultado[:2]
 
    # Convertir la confianza a porcentaje
    try:
        porcentaje = float(confidence_score) * 100
    except ValueError:
        porcentaje = 0  # Si no es un número válido, asignamos 0%
 
    # Eliminar caracteres innecesarios de `class_name` si es necesario
    if len(class_name) > 2:
        class_name = class_name[2:].strip()
 
    # Crear embed con los resultados
    embed = discord.Embed(
        title="Resultados de Clasificación",
        description=f"**Clase:** {class_name}\n**Confianza:** {porcentaje:.2f}%",
        color=discord.Color.blue()
    )
    embed.set_image(url=attach.url)  
    embed.set_footer(text="Clasificación realizada con Keras y TensorFlow.")
 
    await ctx.send(embed=embed)
 
# Ejecutar el bot
bot.run(token)