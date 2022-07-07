#---------------
#MODULES
#pip install discord
#pip install json
#----------------
from http import client
import discord #Module python
import json #Pour le fichier prefixes
from discord.ext import commands #Module python
from discord_slash import SlashCommand #Pour mettre les commandes en /hackcess au lieu de hackcess
#from discord_slash.utils.manage_commands import create_option, create_choice 
import youtube_dl #Pour recupérer des zic de youtube
import asyncio
import os



#PARTIE FONCTION CLASS

class TempsConverter(commands.Converter): #Pour le temp ban création de class TempsConverter
    async def convert (self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]
        
        if amount.isdigit() and unit in ['s','m','h','d']:
            return(int(amount), unit)
        
        raise commands.BadArgument(message='Durée non valide') #En cas de mauvais arguments envoyer message .


    

#CONF GENERAL
HACKCESSTOKENBOT = '' #Variable TOKEN 



def prefix(hackcessbot, message):
    with open('prefixes.json' ,'r')as file: #Lis le fichier prefixes.json
        prefixes = json.load(file)
        
    return prefixes[str(message.guild.id)]
    

hackcessbot = commands.Bot(command_prefix= prefix,help_command=None) #prefix du bot + Commande help 
#slash = SlashCommand(hackcessbot, sync_commands= True)



@hackcessbot.event 
async def on_ready(): #Quand il est demarrer alors 
    
    statushackcess = discord.Activity(type=discord.ActivityType.watching , name="hackcess.org") #Fonction status
    hackcessstatus = discord.Status.online #Mets le status du bot en ligne
    await hackcessbot.change_presence(status=hackcessstatus,activity= statushackcess) #Affiche status discord avec en ligne + message 
  
    
    #----------------------------------------------------------------------#
    
    #discord.Activity(type=discord.ActivityType.watching , name="hackcess.org") -> Regarde hackcess.org
    #discord.Streaming(name="hackcess.org",url="") 2 arguments. Affiche en direct sur Twitch
    #discord.Game = En train de jouer à
    
    #-----------------------------------------------------------------------#
    #(discord.Status.dnd = Ne pas déranger) Mets le statut du bot en ne pas déranger
    #(discord.Status.idle = Inactif) Mets le statut du bot en inactif
    #(discord.Status.online = En Ligne) Mets le statut du bot en ligne
    #(discord.Status.offline = Invisible) Mets le statut du bot en Invisible
    #-----------------------------------------------------------------------#
    
    print("Fonctionnel") #Permet de savoir si il est allumé ou non et renvoi "fonctionnel" dans le terminal
    #loghackcess = hackcessbot.get_channel(912368572272095263) #Renvoie dans le channel logserv le message en dessous
    #await loghackcess.send("Je suis en marche") #Envoie du message "Je suis en marche" au channel logserv
    
@hackcessbot.event 
async def on_guild_join(guild):
    with open('prefixes.json' ,'r')as file: #Lis le fichier prefixes.json
        prefixes = json.load(file)
        
    prefixes[str(guild.id)] = 'hackcess'  #Valeur par défaut 
    
    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)
        
@hackcessbot.event
async def on_guild_remove(guild):
    with open('prefixes.json' ,'r')as file: #Lis le fichier prefixes.json
        prefixes = json.load(file)
        
    prefixes.pop(str(guild.id))
    
    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)
        
@hackcessbot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="Membres")
    await client.add_roles(member, role)
        
#----------------------------------------#    

#COMMANDE DE BASE

@hackcessbot.command(name="ping") #Savoir ça latence
async def ping(ctx,arg=None):
    if arg =="pong":
          em=discord.Embed(description=f'Beau travail , vous vous etes ping vous-même ', color = 0x008000 ) 
          await ctx.send(embed= em)
    else :
        em=discord.Embed(description=f'Voici ton ping : {round(hackcessbot.latency * 1000 )}ms', color = 0x008000 )
        await ctx.send(embed= em)

@hackcessbot.command(name='aide',aliases=["help","h"]) #Commande help
async def aide(ctx):
   embed = discord.Embed(
       title = 'Aide', #Titre de l'embed 'Aide'
       description = 'Toutes les commandes du bot',
       color = discord.Color.green() #Couleur verte
   )
   embed.set_footer(text=f'Requête faite par - {ctx.author}',icon_url=ctx.author.avatar_url)
   embed.add_field(name='General',value='`credits`')
   embed.add_field(name='Moderation',value='`kick`,`ban`,`tempban`,`unban`,`clear`',inline=False) #Saute une ligne inline=False
   embed.add_field(name='Autre',value='`changeprefix`,`ping`',inline=False) #Saute une ligne inline=False
   await ctx.send(embed=embed)

    


@hackcessbot.command(name="credits")
async def credits(ctx):
    await ctx.message.delete() #Supprime la commande instant
    await ctx.send("Bot discord créer par `Hackcess Version 1.0`")
    
@hackcessbot.command(name="clear") #Commande clear    
@commands.has_permissions(manage_messages=True)#Si permissions de gérér la message alors il peux executer la commande clear
async def clear(ctx, amount:int):
    await ctx.message.delete() #Supprime la commande instant
    await ctx.channel.purge(limit=amount)

@hackcessbot.command(name="changeprefix",aliases=["chprefix"]) #Permet de changer le prefix du bot
@commands.has_permissions(administrator=True) #Si permission admin alors il peux changer le prefix
async def changeprefix(ctx , prefix):
    with open('prefixes.json' ,'r')as file: #Lis le fichier prefixes.json
        prefixes = json.load(file)
            
    prefixes[str(ctx.guild.id)] = prefix
    
    with open('prefixes.json','w') as f:
        json.dump(prefixes, f, indent=4)
        
    em=discord.Embed(description=f'Préfixe remplacé par : **{prefix}**', color = 0x008000 ) 
    await ctx.send(embed= em)


#MUSIQUE COMMANDE
@hackcessbot.command(name="join" ,aliases=["j"]) #Rejoindre un voc
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()
    
@hackcessbot.command(name="leave", aliases=["l"]) #Quittez un voc
async def leave(ctx):
    await ctx.voice_client.disconnect()
    






    
    


    
    
    
   
    
#MODERATION COMMANDE

@hackcessbot.command(name="ban") #COMMANDE BAN
@commands.has_permissions(ban_members=True) #Si permission de ban alors
async def ban(ctx ,member: commands.MemberConverter): #Commande pour ban 
    await ctx.guild.ban(member)
    em = discord.Embed(description = f"**{member}** a été banni 🔨.", color = 0xFF0000) #ENVOIE LE MESSAGE @.... a été banni
    em.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed= em)
    
@hackcessbot.command(name="unban") #COMMANDE UNBAN
@commands.has_permissions(ban_members=True)#Si permission de ban alors
async def unban(ctx,user,*raison):
    userName, userID = user.split("#")
    bannedUsers = await ctx.guild.bans() #Regarde dans la liste des bannis
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userID:
            await ctx.guild.unban(i.user,reason = raison)
            em = discord.Embed(description=f"{user} a été **unban** par **{ctx.author}** !",color = 0x000000)
            await ctx.send(embed= em)
            return
    await ctx.send(f"{user} ne figure pas dans la liste des utilisateurs bannis.")
        
@hackcessbot.command() #COMMANDE TEMPBAN
@commands.has_permissions(manage_messages=True) #Si permission de gérer message alors il peut
async def tempban(ctx ,member: commands.MemberConverter , duration : TempsConverter): #Commande pour tempban 
    
    multiplier = {'s':1, 'm':60, 'h':3600,'d': 86400} #Minute = 60 secondes / 1h = 3600 secondes / 1jour = 86400 seconde
    amount, unit = duration 
    
    await ctx.guild.ban(member)
    em = discord.Embed(description = f"**{member}** a été banni pour **{amount}{unit}🔨**.", color = 0xFFFFFF ) #ENVOIE LE MESSAGE @.... a été banni en embed
    em.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed= em)
    await asyncio.sleep(amount * multiplier[unit]) #PERMET DE GERER LE TEMPS DU BAN
    await ctx.guild.unban(member) #Une fois le délais dépasser il deban la personne 
    em=discord.Embed(description=f"**{member}** à été debanni", color = 0x008000)
    em.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed= em)
    
    
@hackcessbot.command(name="kick") #Commande Kick 
@commands.has_permissions(manage_messages=True) #Si permission de gérer message alors il peut
async def kick(ctx, user : discord.User ,*,raison = "Aucune raison n'a été renseignée!"): #Si aucune raison ecrire  "Aucune raison n'a été renseignée!"
    await ctx.guild.kick(user, reason = raison)
    
    em = discord.Embed(description= f"{user.mention} a été **kick** pour **{raison}** par {ctx.author} !" , color = 0xFFFFFF ) #Embed discord
    em.set_thumbnail(url = user.avatar_url) #On recupere la photo de profil de la personne kick
    
    await ctx.send(embed= em)
  
    
#GESTION DES ERREURS
    
@clear.error #En cas d'erreur sur la commande hackcess clear
async def clear_error(ctx , error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Veuillez spécifier une quantité de message à supprimer ```exemple : hackcess clear 1 ``` ') #Specifiez un nombre , exemple hackcess clear 1
    
@hackcessbot.event 
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): #Si commande inexistante
         em = discord.Embed(description=f'**⚠️ERROR 404 Commande invalide⚠️**') #Envoie cet phrase
         await ctx.send(embed= em)
        




    
#LANCEMENT DU BOT    
hackcessbot.run(HACKCESSTOKENBOT) #Mettre le token pour bien démarrer le bot , le token se trouve dans la variable HACKCESSTOKENBOT


#01001000 01000001 01000011 01001011 01000011 01000101 01010011 01010011 
