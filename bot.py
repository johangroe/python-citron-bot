# coding: utf-8

import discord
import time
import random
from webapp import keep_alive

## wachbleiben hält den bot 24/7 am laufen, anleitung nach:
##https://replit.com/talk/learn/Hosting-discordpy-bots-with-replit/11008
## aufrufen vor client.run() ist wichtig!


TOKEN = "--Your--Bot--Token--Here"

beleidigungen_in_nutzung = []

## befehle "normal" (befehle halt an sich ne...)
tags_schimpfen = ["beleidige", "beschimpfe", "ärgere"]
tags_hilfe = ["help", "hilfe", "befehle", "commands"]
tags_status = ["state", "status", "stats"]
tags_aufhoeren = ["aufhören", "anhalten"]
tags_weitermachen = ["weiter", "weitermachen"]
tags_timeout = ["timeout", "timout", "to"]
tags_nicht = ["nicht", "ausnehmen", "ausschließen"]
tags_doch = ["doch", "einschließen", "erlauben", "erlaube"]
tags_addop = ["addop"]
tags_deop = ["deop"]
tags_online = ["online", "hello"]
tags_statusfull = ["statusfull", "statuskomplett", "sf"]
tags_befehle_full = ["befehlefull", "befehlekomplett", "commandsfull"]
tags_delete = ["lösche", "löschen", "delete", "clean", "clear"]
tags_anschalten = ["anschalten", "startup", "hochfahren"]
tags_ausschalten = ["ausschalten", "shutdown", "herunterfahren"]
tags_aktivitaet = ["aktivität", "activity", "erscheinung", "appearance"]
tags_prefix = ["prefix", "präfix"]

## ergänzungen zu !aktivität
tags_aktivit_reset = ["reset", "zurücksetzen", "rücksetzen"]
tags_aktivit_game = ["game", "spiel", "spielen", "spielt"]
tags_aktivit_movie = ["movie", "film", "schaut", "schauen"]
tags_aktivit_music = ["musik", "hören", "zuhören", "hört", "music"]
tags_aktivitaeten_alle = ["reset", "zurücksetzen", "rücksetzen", "game", "spiel", "spielen", "spielt", "movie", "film", "schaut", "schauen", "musik", "hören", "zuhören", "hört", "music"]

## ergänzungen zu !op
tags_op_allgemein = ["general", "allgemein", "normal", "normie"]
tags_op_nutzer = ["mitglieder", "nutzer", "personen", "menschen"]
tags_op_aktivitaet = ["aktivität", "appearance", "erscheinung", "activity"]
tags_op_all = ["all", "alles", "komplett", "full"]
tags_op_zusammenfassung = ["general", "allgemein", "normal", "normie", "mitglieder", "nutzer", "personen", "menschen", "aktivität", "appearance", "erscheinung", "activity", "all", "alles", "komplett", "full"]

## alle befehle, die mit Adminrechten ausgeführt werden können
tags_op = ["aufhören", "anhalten", "timeout", "timout", "to", "weitermachen", "weiter", "nicht", "ausnehmen", "ausschließen", "doch", "einschließen", "erlauben", "erlaube", "addop", "deop", "statusfull", "statuskomplett", "befehlefull", "befehlekomplett", "commandsfull", "online", "hello", "lösche", "löschen", "delete", "clean", "clear", "anschalten", "startup", "hochfahren", "ausschalten", "shutdown", "herunterfahren", "aktivität", "activity", "erscheinung", "appearance", "prefix", "präfix"]

##
prefixe = ["!", "$", "/", ".", "?", "#", "-"]
stop = False
deleted_op_message = False
needed_time = 0
actual_time = 0
to_triggered = False
online = True
last_active = ""
prefix = "!"
#last_activity_type = "game"
#last_activity_content =  "besser als alle"




client = discord.Client()

@client.event
async def on_ready():
    global needed_time, actual_time, last_activity_type, last_activity_content
    actual_time = round(time.time(),0)
    needed_time = actual_time

    print(f"{client.user} is connected.")

    ## berechtigungen / admins / verbotene personen / letzte aktivität
    f = open("stuff.txt")
    admins_file = f.readline()
    admins_file_splitted = admins_file.split(" ")
    waste = admins_file_splitted.pop(0)
    waste = admins_file_splitted.pop(-1)
    admins = admins_file_splitted
    

    not_auth_file = f.readline()
    not_auth_file_splitted = not_auth_file.split(" ")
    waste = not_auth_file_splitted.pop(0)
    waste = not_auth_file_splitted.pop(-1)
    not_authorized = not_auth_file_splitted
    

    activities_file = f.readline()
    activities_file_splitted = activities_file.split(" ")
    waste = activities_file_splitted.pop(0)
    waste = activities_file_splitted.pop(-1)
    activities = activities_file_splitted
    
    last_activity_type = activities.pop(0)
    last_activity_content = " ".join(activities)

    prefix_file = f.readline()
    prefix_file_splitted = prefix_file.split(" ")
    prefix = prefix_file_splitted[1]

    f.close()

    print(prefix)


    if last_activity_type == "game":
        await client.change_presence(activity=discord.Game(name=last_activity_content))
    elif last_activity_type == "movie":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=last_activity_content))
    elif last_activity_type == "music":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=last_activity_content))
    elif last_activity_type == "none":
        await client.change_presence(activity = None)

    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="anderen beim Umziehen zu"))
    



@client.event
async def on_message(message):
    global stop, deleted_op_message, admins, not_authorized, needed_time, actual_time, admins, not_authorized, to_triggered, online, last_activity_content, last_activity_type, last_active

    
    if message.author == client.user:
        return

    ## timeout beenden
    if to_triggered == True:
        actual_time = round(time.time(),0)
        if needed_time > actual_time:
            stop = True
        elif needed_time <= actual_time:
            stop = False
            to_triggered = False

    
    
    ## berechtigungen / admins / verbotene personen / letzte aktivität
    f = open("stuff.txt")
    admins_file = f.readline()
    admins_file_splitted = admins_file.split(" ")
    waste = admins_file_splitted.pop(0)
    waste = admins_file_splitted.pop(-1)
    admins = admins_file_splitted
    #print("admins:" + str(admins))

    not_auth_file = f.readline()
    not_auth_file_splitted = not_auth_file.split(" ")
    waste = not_auth_file_splitted.pop(0)
    waste = not_auth_file_splitted.pop(-1)
    not_authorized = not_auth_file_splitted
    #print("not_authorized:" + str(not_authorized))
    
    waste = f.readline()

    prefix_file = f.readline()
    prefix_file_splitted = prefix_file.split(" ")
    prefix = prefix_file_splitted[1]

    f.close()


    ## einzelne wörter / nachrichtenverarbeitung
    message_ori = message.content
    message_split = message_ori.split(" ")
    message_chars = list(str(message_split[0]))
    prefix_sent = message_chars.pop(0)
    waste = list(str(message_split[0]))
    waste.pop(0)
    waste2 = message_split
    waste3 = waste2.pop(0)
    message_split = [str("".join(waste))]
    message_split.extend(waste2)
    

    ## richtiger prefix
    if prefix_sent != prefix:
        if prefix_sent in prefixe and (str(message_split[0]).lower() in tags_status or str(message_split[0]).lower() in tags_statusfull or str(message_split[0]).lower() in tags_prefix or str(message_split[0]).lower() in tags_online):
           pass
        else:
            return



    ## op command in textchannel
    if str(message_split[0]).lower() in tags_op:
        if str(message.channel.type) == "text":
            await message.channel.purge(limit=1)
            deleted_op_message = True
            if message.author.name in admins:
                await message.author.send("KEINE OP-COMMANDS IN TEXTCHANNELS!!!  NUR DM!")

    
    ## op stuff hilfe
    if str(message_split[0]).lower() == "op":
        try: 
            await message.channel.purge(limit=1)
        except AttributeError:
            pass

        if message.author.name in admins:
            if len(message_split) > 1 and str(message_split[1]).lower() not in tags_op_zusammenfassung:
                send_warning = False
                await message.author.send("Bitte einen richtigen Sektor nach !op angeben...")
    
            elif len(message_split) == 1:
                send_warning = True
                embed = discord.Embed(title = "Normie-Commands für CitronBot", description = "")
                embed.add_field(name = str(prefix) + "beleidige <Name>", value = "Beleidigt die Person")
                embed.add_field(name = str(prefix) + "hilfe", value = "Ruft die Normie-Hilfe auf")
                embed.add_field(name = str(prefix) + "status", value = "Zeigt den aktuellen Status des Bots")
                embed.add_field(name = str(prefix) + "op <Sektor>", value = "Ruft diese Nachricht auf\nSektoren: allgemein, mitglieder, aktivität, alles")
                await message.author.send(content = None, embed = embed)
             
            elif len(message_split) > 1 and str(message_split[1]).lower() in tags_op_zusammenfassung:
                send_warning = True
                if str(message_split[1]).lower() in tags_op_allgemein:
                    embed = discord.Embed(title = "OP-Commands (Allgemein) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "aufhören", value = "Hält den Bot auf unbestimmte Zeit an (Bot bleibt online!)")
                    embed.add_field(name = str(prefix) + "weitermachen", value = "Setzt den Bot fort")
                    embed.add_field(name = str(prefix) + "timeout <Zeit in Minuten, dahinter Sekunden, getrennt durch Leerzeichen>", value = "hält den Bot für die bestimmte Zeit an, kann durch !weitermachen gebrochen werden")
                    embed.add_field(name = str(prefix) + "ausschalten", value = "Setzt den Bot künstlich auf offline")
                    embed.add_field(name = str(prefix) + "anschalten", value = "Setzt den Bot auf online")
                    embed.add_field(name = str(prefix) + "statusfull", value = "Zeigt den aktuellen Status des Bots (Komplett)")
                    embed.add_field(name = str(prefix) + "befehlefull", value = "Zeigt ALLE Befehle und deren Alternates an")
                    embed.add_field(name = str(prefix) + "lösche <Zahl>", value = "Durchsucht die angegebene Zahl von Nachrichten nach Bot-Nachr. und löscht diese")
                    embed.add_field(name = str(prefix) + "online", value = "Kurze Abfrage, ob der Bot online ist und funktioniert")
                    embed.add_field(name = str(prefix) + "prefix <gew. Präfix>", value = "Ändert den Präfix des Bots, erlaubt sind: " + 
                    str(prefixe[0]) + "  " + str(prefixe[1]) + "  " + str(prefixe[2]) + "  " + str(prefixe[3]) + "  " + str(prefixe[4]) + "  " + str(prefixe[5]) + "  " + str(prefixe[6]))
                    await message.author.send(content = None, embed = embed)
                
                elif str(message_split[1]).lower() in tags_op_nutzer:
                    embed = discord.Embed(title = "OP-Commands (Nutzerverwaltung) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "nicht <Discord-Name (ohne #1234)>", value = "Bannt diesen Nutzer")
                    embed.add_field(name = str(prefix) + "doch <Discord-Name (ohne #1234)>", value = "Entbannt diesen Nutzer")
                    embed.add_field(name = str(prefix) + "addop <Discord-Name (ohne #1234)>", value = "Diesen Benutzer als Admin hinzufügen")
                    embed.add_field(name = str(prefix) + "deop <Discord-Name (ohne #1234)>", value = "Diesen Benutzer von den Admins entfernen")
                    await message.author.send(content = None, embed = embed)
            
                elif str(message_split[1]).lower() in tags_op_aktivitaet:
                    embed = discord.Embed(title = "OP-Commands (Aktivitäten/Erscheinungsbild) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "aktivität <Aktivität> <Inhalt>", value = "Ändert die Aktivität des Bot")
                    embed.add_field(name = "<'reset'>", value = "Löscht die personalisierte Aktivität")
                    embed.add_field(name = "<'spielt'> <Inhalt>", value = "Personalisierte Aktivität: 'Spielt (Inhalt)'")
                    embed.add_field(name = "<'schaut'> <Inhalt>", value = "Personalisierte Aktivität: 'Schaut (Inhalt)'")
                    embed.add_field(name = "<'hört'> <Inhalt>", value = "Personalisierte Aktivität: 'Hört (Inhalt) zu'")
                    await message.author.send(content = None, embed = embed)
            
            
                    
                
                elif str(message_split[1]).lower() in tags_op_all:

                    embed = discord.Embed(title = "Normie-Commands für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "beleidige <Name>", value = "Beleidigt die Person")
                    embed.add_field(name = str(prefix) + "hilfe", value = "Ruft die Normie-Hilfe auf")
                    embed.add_field(name = str(prefix) + "status", value = "Zeigt den aktuellen Status des Bots")
                    embed.add_field(name = str(prefix) + "op <Sektor>", value = "Ruft diese Nachricht auf\nSektoren: allgemein, mitglieder, aktivität, alles")
                    await message.author.send(content = None, embed = embed)

                    embed = discord.Embed(title = "OP-Commands (Allgemein) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "aufhören", value = "Hält den Bot auf unbestimmte Zeit an (Bot bleibt online!")
                    embed.add_field(name = str(prefix) + "weitermachen", value = "Setzt den Bot fort")
                    embed.add_field(name = str(prefix) + "timeout <Zeit in Minuten, dahinter Sekunden, getrennt durch Leerzeichen>", value = "hält den Bot für die bestimmte Zeit an, kann durch !weitermachen gebrochen werden")
                    embed.add_field(name = str(prefix) + "ausschalten", value = "Setzt den Bot künstlich auf offline")
                    embed.add_field(name = str(prefix) + "anschalten", value = "Setzt den Bot auf online")
                    embed.add_field(name = str(prefix) + "statusfull", value = "Zeigt den aktuellen Status des Bots (Komplett)")
                    embed.add_field(name = str(prefix) + "befehlefull", value = "Zeigt ALLE Befehle und deren Alternates an")
                    embed.add_field(name = str(prefix) + "lösche <Zahl>", value = "Durchsucht die angegebene Zahl von Nachrichten nach Bot-Nachr. und löscht diese")
                    embed.add_field(name = str(prefix) + "online", value = "Kurze Abfrage, ob der Bot online ist und funktioniert")
                    embed.add_field(name = str(prefix) + "prefix <gew. Präfix>", value = "Ändert den Präfix des Bots, erlaubt sind: " + 
                    str(prefixe[0]) + "  " + str(prefixe[1]) + "  " + str(prefixe[2]) + "  " + str(prefixe[3]) + "  " + str(prefixe[4]) + "  " + str(prefixe[5]) + "  " + str(prefixe[6]))
                    await message.author.send(content = None, embed = embed)

                    embed = discord.Embed(title = "OP-Commands (Nutzerverwaltung) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "nicht <Discord-Name (ohne #1234)>", value = "Bannt diesen Nutzer")
                    embed.add_field(name = str(prefix) + "doch <Discord-Name (ohne #1234)>", value = "Entbannt diesen Nutzer")
                    embed.add_field(name = str(prefix) + "addop <Discord-Name (ohne #1234)>", value = "Diesen Benutzer als Admin hinzufügen")
                    embed.add_field(name = str(prefix) + "deop <Discord-Name (ohne #1234)>", value = "Diesen Benutzer von den Admins entfernen")
                    await message.author.send(content = None, embed = embed)

                    embed = discord.Embed(title = "OP-Commands (Aktivitäten/Erscheinungsbild) für CitronBot", description = "")
                    embed.add_field(name = str(prefix) + "aktivität <Aktivität> <Inhalt>", value = "Ändert die Aktivität des Bot")
                    embed.add_field(name = "<'reset'>", value = "Löscht die personalisierte Aktivität")
                    embed.add_field(name = "<'spielt'> <Inhalt>", value = "Personalisierte Aktivität: 'Spielt (Inhalt)'")
                    embed.add_field(name = "<'schaut'> <Inhalt>", value = "Personalisierte Aktivität: 'Schaut (Inhalt)'")
                    embed.add_field(name = "<'hört'> <Inhalt>", value = "Personalisierte Aktivität: 'Hört (Inhalt) zu'")
                    await message.author.send(content = None, embed = embed)
            
            if send_warning == True:
                embed = discord.Embed(title = "WICHTIG: NIE die OP-Commands in Textchannel senden, nur DM an Bot!!!")
                await message.author.send(content = None, embed = embed)


            
            
    
    
    



    ## beleidigungs stuff

    if len(beleidigungen_in_nutzung) == 0:
        beleidigungen_in_nutzung.extend([", du bildungsresistenter Intelligenzallergiker.", 
        ", du bist nicht dumm, du denkst nur anders.", 
        ", gibt’s dich auch in Nicht-Scheiße?", 
        ", du bist wie Montagmorgen. Keiner mag dich!", 
        ", schöne Zähne hast du. Gabs die auch in weiß?", 
        ", deine Haut gleicht der einer achtjährigen Apfelsine.", 
        ", du bist so dünn, bewirb dich doch als Maskottchen für die Welthungerhilfe.", 
        ", du bist genauso sinnvoll wie ein Sandkasten in der Sahara.", 
        ", du bist zu allem fähig, bist aber für nichts zu gebrauchen.", 
        ", ich habe ein Foto von dir an der Kellertür – So kommen mir keine Ratten ins Haus!", 
        ", ich würde mich ja geistig mit dir duellieren, aber wie ich sehe bist du unbewaffnet.", 
        ", ein Tag ohne dich gleicht einem Monat Urlaub.", 
        ", es gibt fast 6 Milliarden Menschen, und ich muss ausgerechnet dir begegnen.", 
        ", wenn Du eine Fliege verschluckst, ist mehr Gehirn in deinem Bauch als in deinen Kopf.", 
        ", ohne dich ist alles schöner.", 
        ", ist Dein Clown-Kostüm in der Reinigung?", 
        ", als Dein Vater dich gesehen hat, erschoss er den Storch!", 
        ", siehst wie ein Versuch aus. Sind Deine Eltern Chemiker?", 
        ", schön, dass du da bist – Und nicht hier!", 
        ", du wurdest wohl auch mit einem Stück Brot vom Baum gelockt.", 
        ", wenn Blödheit bremsen würde, könntest du dich den ganzen Tag nicht von der Stelle bewegen!", 
        ", deine Geburt war ein riesen Beitrag zur Umweltverschmutzung.", 
        ", nach deiner Geburt hat der Arzt dich wohl dreimal hochgeworfen aber nur zweimal aufgefangen!", 
        ", wenn ich du wäre, würde ich lieber ich sein wollen!", 
        ", es wird schon dunkel, solltest du nicht wieder zurück zu den Müllsäcken?", 
        ", was kannst Du als Unbeteiligter zum Thema Intelligenz sagen?", 
        ", du ähnelst einer Wolke: Wenn du dich verziehst, kann es doch noch ein schöner Tag werden!", 
        ", du bist gaziel wie eine Gazelle, oder wie heißt das Tier mit dem Rüssel?!", 
        ", schau doch mal wieder vorbei, wenn du weniger Zeit hast!", 
        ", wären deine Eltern besser mal 5 Minuten spazieren gegangen.", 
        ", ich habe gar nicht gewusst, dass man Scheiße so hoch stapeln kann!", 
        ", mal unter uns, ich kenne einen super Gesichtschirurgen!", 
        ", du siehst aus als wärst du aufgestanden und weggegangen.", 
        ", dein Geburtstag steht im Geschichtsbuch gleich nach Hiroshima und Tschernobyl!", 
        ", wenn dein Gesicht auf einer Briefmarke wäre, würde die Post Pleite gehen.", 
        ", ich bin in einer halben Stunde wieder da, du kannst ja so lange mal bis 10 zählen.", 
        ", hatte Kurt Cobain dich gekannt, hätte er sich glatt nochmal erschossen!", 
        ", könntest du dich bitte einfach in eine Ecke legen und sterben? Aber leise bitte, ich muss hier arbeiten.", 
        ", wenh Dummheit weh tun würde, hättest du den ganzen Tag schmerzen.", 
        ", hätte mein Hund dein Gesicht, würde ich ihm den Arsch rasieren und beibringen rückwärts zu laufen!", 
        ", wenn ich dein Gesicht so sehe, gefällt mir mein Arsch immer besser.", 
        ", du hast schon was drauf, auch wenn es nur Zahnbelag ist!", 
        ", du hast doch gerade genug Gehirnzellen, um nicht ins Wohnzimmer zu kacken.", 
        ", ich habe gar nicht gewusst, dass man Scheiße so hoch stapeln kann!"])

    
    
    
    #print(message_split)


    ## beleidigungs-sender

    if stop == False and message.author.name not in not_authorized:
        if online == True:
            if message_split[0] == "!ping":
                await message.channel.send("!pong")

            if len(message_split) != 1:
                #name = str.title(message_split[1])
                name_list = []
                #i = 1
                #for i in range(len(message_split)):
                    
                name_list.extend(message_split)
                name_list.pop(0)
                name = ""
                i = 1
                for i in range(len(name_list)):
                    
                    name = name + str.title(name_list[i])
                    name = name + " "
                    i += 1
                    #print("triggered")

                index_beleidigung = random.randint(1, len(beleidigungen_in_nutzung)) - 1
                beleidigung = beleidigungen_in_nutzung.pop(index_beleidigung)
                #print(message_split)

            if message_split[0] in tags_schimpfen and len(message_split) > 1:
                await message.channel.send("Ey " + name + beleidigung)

            elif message_split[0] in tags_schimpfen and len(message_split) == 1:
                await message.channel.send("Du musst schon nen Namen dahinter schreiben du Pfosten!")
            
            else:
                #print(message_split)
                #print(tags_schimpfen)
                #print(len(message_split))
                #print("gar nichts")
                pass


            ## hilfe normie

            if str(message_split[0]).lower() in tags_hilfe:
                #print("hilfe angefordert")
                embed = discord.Embed(title = "Hilfe für CitronBot", description = "")
                embed.add_field(name = "!beleidige <Name>", value = "Beleidigt die Person")
                embed.add_field(name = "!hilfe", value = "Ruft diese Nachricht auf")
                embed.add_field(name = "!status", value = "Zeigt den aktuellen Status des Bots an (online, etc.)")
                embed.add_field(name = "---", value = "... und halt !op")
                await message.channel.send(content = None, embed = embed)

        ## status normie
        if str(message_split[0]).lower() in tags_status:
            embed = discord.Embed(title = "Status:", description = "")
            if online == True:
                embed.add_field(name = "online:", value = ":white_check_mark:")
                if stop == True and to_triggered == True:
                    embed.add_field(name = "pausiert:", value = ":white_check_mark: " + str(round(needed_time - actual_time)) + " sec")
                elif stop == True and to_triggered == False:
                    embed.add_field(name = "pausiert:", value = ":white_check_mark: dauerhaft")
                elif stop == False:
                    embed.add_field(name = "pausiert:", value = ":x:")
                embed.add_field(name = "Präfix:", value = prefix)
            elif online == False:
                embed.add_field(name = "online:", value = ":x:")
            
            await message.channel.send(content = None, embed = embed)
    
    
    ### OP COMMANDS ###
    if deleted_op_message == False:
        ## anhalten, timeout, weitermachen
        if (message.author.name in admins) and (deleted_op_message == False):
            
            if str(message_split[0]).lower() in tags_aufhoeren:
                stop = True
                to_triggered = False
                await message.author.send("Der Bot wurde angehalten...")

            elif str(message_split[0]).lower() in tags_weitermachen:
                stop = False
                to_triggered = False
                await message.author.send("Der Bot wird fortgesetzt...")
                
            if str(message_split[0]).lower() in tags_timeout:
                if len(message_split) == 1:
                    await message.author.send("Bitte eine Zeit dahinterschreiben, wie lange der Bot pausiert sein soll!")
                elif len(message_split) > 1:
                    if message_split[1].isnumeric():
                        if len(message_split) == 3:
                            if message_split[2].isnumeric():
                                #print("zeit richtig angegeben")
                                to_mins = float(message_split[1])
                                to_secs = float(message_split[2])
                                difference = needed_time - actual_time
                                actual_time = round(time.time(),0)
                                needed_time = actual_time + to_secs + (to_mins*60)
                                if difference >= 0:
                                    needed_time = needed_time + difference
                                to_triggered = True
                                #print(actual_time)
                                #print(needed_time)
                                #print(difference)
                                
                                ## timeout kombiniert

                        elif len(message_split) == 2:
                            #print("zeit richtig angegeben")
                            to_mins = float(message_split[1])
                            difference = needed_time - actual_time
                            actual_time = round(time.time(),0)
                            needed_time = actual_time + (to_mins*60)
                            if difference >= 0:
                                needed_time = needed_time + difference
                            to_triggered = True
                            ## timeout bloß minuten
                        
                        await message.author.send("Aktuelles Timeout: " + str(round(needed_time - actual_time)) + " sec")
                            	
                    else:
                        await message.author.send("Bitte Zeit als Zahl angeben (einfach Zahl in Minuten und dahinter Sekunden, getrennt durch Leerzeichen)")
                


                
            ## erlaubt, nicht erlaubt

            if str(message_split[0]).lower() in tags_nicht:
                if len(message_split) > 1:
                    not_authorized.append(message_split[1])
                    await message.author.send(message_split[1] + " wurde vom Bot ausgeschlossen.")
                elif len(message_split) == 1:
                    await message.author.send("Bitte einen Namen nach dem Befehl angeben...")
            
            if str(message_split[0]).lower() in tags_doch:
                if len(message_split) > 1:
                    if message_split[1] in not_authorized:
                        not_authorized.remove(message_split[1])
                        await message.author.send(message_split[1] + " wurde der Bot erlaubt.")
                    elif message_split[1] not in not_authorized:
                        await message.author.send(message_split[1] + " wurde nicht gefunden als nicht erlaubt, check mal Schreibweise und auch die Liste der nicht Erlaubten mit !statusfull ab...")
                elif len(message_split) == 1:
                    await message.author.send("Bitte einen Namen nach dem Befehl angeben...")



            ## addop deop

            if str(message_split[0]).lower() in tags_addop:
                if len(message_split) > 1:
                    admins.append(message_split[1])
                    await message.author.send(message_split[1] + " ist jetzt ein Admin.")
                elif len(message_split) == 1:
                    await message.author.send("Bitte einen Namen nach dem Befehl angeben...")
            
            if str(message_split[0]).lower() in tags_deop:
                if len(message_split) >  1:
                    if str(message_split[1]).lower() != "nino":
                        if message_split[1] in admins:
                            admins.remove(message_split[1])
                            await message.author.send(message_split[1] + " ist jetzt kein Admin mehr.")
                        elif message_split[1] not in admins:
                            await message.author.send(message_split[1] + " wurde nicht als Admin gefunden, check mal Schreibweise und auch die Adminliste mit !statusfull ab...")
                    elif str(message_split[1]).lower() == "nino":
                        await message.author.send(message_split[1].title() + " kann nicht gelöscht werden, da er ein Ehrenmann ist (wäre ja auch zu schön, ne?)")
                elif len(message_split) == 1:
                    await message.author.send("Bitte einen Namen nach dem Befehl angeben...")

            
            

            ## statusfull
            if str(message_split[0]).lower() in tags_statusfull:

                embed = discord.Embed(title = "Komplettstatus CitronBot", description = " ")
                if online == True:
                    embed.add_field(name = "online:", value = ":white_check_mark:")
                elif online == False:
                    embed.add_field(name = "online:", value = ":x:\n(versteckt online)")
                if stop == True and to_triggered == True:
                    embed.add_field(name = "pausiert:", value = ":white_check_mark: " + str(round(needed_time - actual_time)) + " sec")
                elif stop == True and to_triggered == False:
                    embed.add_field(name = "pausiert:", value = ":white_check_mark: dauerhaft")
                elif stop == False:
                    embed.add_field(name = "pausiert:", value = ":x:")
                embed.add_field(name = "Admins:", value = ", ".join(admins))
                carry = str(", ".join(not_authorized))
                if len(not_authorized) == 0:
                    carry = "Keine"
                embed.add_field(name = "Gebannte:", value = carry)
                embed.add_field(name = "Präfix:", value = prefix)
                
                if last_activity_type == "none":
                    embed.add_field(name = "Aktivität: ", value = "keine")
                elif last_activity_type != "none":
                    if last_activity_type == "game":
                        activity = "Spielt " + str(last_activity_content)
                    elif last_activity_type == "movie":
                        activity = "Schaut " + str(last_activity_content)
                    elif last_activity_type == "music":
                        activity = "Hört " + str(last_activity_content) + " zu"
                    embed.add_field(name = "Aktivität:", value = activity)
                await message.author.send(content = None, embed = embed)
                

            ## commands full

            if str(message_split[0]).lower() in tags_befehle_full:

                embed = discord.Embed(title = "Komplettbefehle normal CitronBot", description = " ")
                embed.add_field(name = str(prefix) + "beleidige <Name>", value = str(prefix) + "beschimpfe <>\n" + str(prefix) + "ärgere <>")
                embed.add_field(name = str(prefix) + "hilfe", value = str(prefix) + "help\n" + str(prefix) + "befehle\n" + str(prefix) + "commands")
                embed.add_field(name = str(prefix) + "status", value = str(prefix) + "state")
                embed.add_field(name = str(prefix) + "op", value = "-----")
                await message.author.send(content = None, embed = embed)
                embed = discord.Embed(title = "Komplettbefehle OP CitronBot", description = " ")
                embed.add_field(name = str(prefix) + "aufhören", value = str(prefix) + "anhalten")
                embed.add_field(name = str(prefix) + "timeout <min> <sec>", value = str(prefix) + "timout <> <>\n" + str(prefix) + "to <> <>")
                embed.add_field(name = str(prefix) + "weitermachen", value = str(prefix) + "weiter")
                embed.add_field(name = str(prefix) + "nicht <Discord-Name>", value = str(prefix) + "ausnehmen <>\n" + str(prefix) + "ausschließen <>")
                embed.add_field(name = str(prefix) + "doch <Discord-Name>", value = str(prefix) + "einschließen <>\n" + str(prefix) + "erlauben <>\n" + str(prefix) + "erlaube")
                embed.add_field(name = str(prefix) + "addop <Discord-Name>", value = "-----")
                embed.add_field(name = str(prefix) + "deop <Discord-Name>", value = "-----")
                embed.add_field(name = str(prefix) + "statusfull", value = str(prefix) + "statuskomplett\n" + str(prefix) + "sf")
                embed.add_field(name = str(prefix) + "befehlefull", value = str(prefix) + "befehlekomplett\n" + str(prefix) + "commandsfull")
                embed.add_field(name = str(prefix) + "lösche <Zahl>", value = str(prefix) + "löschen <>\n" + str(prefix) + "delete <>\n" + str(prefix) + "clean <>\n" + str(prefix) + "clear")
                embed.add_field(name = str(prefix) + "anschalten", value = str(prefix) + "startup\n" + str(prefix) + "hochfahren")
                embed.add_field(name = str(prefix) + "ausschalten", value = str(prefix) + "shutdown\n" + str(prefix) + "herunterfahren")
                embed.add_field(name = str(prefix) + "aktivität <Akt.> <Inhalt>", value = str(prefix) + "activity <> <>\n" + str(prefix) + "erscheinung <> <>\n" + str(prefix) + "appearance <> <>")
                embed.add_field(name = "Aktivitäten", value = "<reset>\n<game, spiel, spielen, spielt>\n<movie, film, schaut, schauen>\n<musik, hören, zuhören, hört, music>")
                embed.add_field(name = str(prefix) + "online", value = str(prefix) + "hello")
                embed.add_field(name = str(prefix) + "prefix", value = "-----")
                await message.author.send(content = None, embed = embed)


            ## online?
            if str(message_split[0]).lower() in tags_online:
                if online == True:
                    embed = discord.Embed(title = "Yep, bin online :upside_down:")
                    embed.add_field(name = "Kannst " + str(prefix_sent) + str(message_split[0]) + " löschen...", value = " . ")
                    await message.author.send(content = None, embed = embed)

                elif online == False:
                    embed = discord.Embed(title = "Yep, bin online, aber unsichtbar :shushing_face:")
                    embed.add_field(name = "Kannst " + str(prefix_sent) + str(message_split[0]) + " löschen...", value = " . ")
                    await message.author.send(content = None, embed = embed)

                time.sleep(3)
                #await message.channel.purge(limit=1)

                dmchannel = message.channel
                async for message in dmchannel.history(limit=1):
                    if message.author == client.user:
                        await message.delete()

            ## nachrichten löschen
            if str(message_split[0]).lower() in tags_delete:
                if len(message_split) == 1:
                    await message.author.send("Du musst schon ne Zahl dahinterschreiben...")
                    pass
                
                elif len(message_split) > 1:
                    try:
                        anzahl = int(message_split[1])
                    except ValueError:
                        await message.author.send("Du musst schon ne ganze Zahl dahinter schreiben...")
                        pass
                
                anzahl = int(message_split[1])
                dmchannel = message.channel
                async for message in dmchannel.history(limit = anzahl):
                    if message.author == client.user:
                        await message.delete()

            ## online offline
            if str(message_split[0]).lower() in tags_ausschalten:
                online = False
                await client.change_presence(status = discord.Status.offline)
                await message.author.send("Herunterfahren...")
            
            elif str(message_split[0]).lower() in tags_anschalten:
                online = True
                await client.change_presence(status = discord.Status.online)
                await message.author.send("Hochfahren...")

                if last_activity_type == "game":
                    await client.change_presence(activity=discord.Game(name=last_activity_content))
                elif last_activity_type == "movie":
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=last_activity_content))
                elif last_activity_type == "music":
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=last_activity_content))
                elif last_activity_type == "none":
                    await client.change_presence(activity = None)
            

            ## prefix wechseln

            if str(message_split[0]).lower() in tags_prefix:
                if len(message_split) > 1:
                    if str(message_split[1]) in prefixe:
                        prefix = message_split[1]
                        await message.author.send("Präfix geändert...")
                    else:
                        await message.author.send("Bitte gültigen Präfix angeben...")
                else:
                    await message.author.send("Bitte gültigen Präfix angeben...")


            ## aktivität status spiel whatever
            if str(message_split[0]).lower() in tags_aktivitaet:
                #print(message_split)
                
                if len(message_split) == 1:
                    await message.author.send("Du musst schon eine Aktivität nach dem Befehl angeben...")
                
                elif len(message_split) == 2 and str(message_split[1]) not in tags_aktivit_reset:
                    await message.author.send("Du musst schon eine Aktivität nach " + message_split[1] + " angeben...")
                
                elif str(message_split[1]).lower() not in tags_aktivitaeten_alle:
                    await message.author.send("Du musst schon eine richtige Aktivität angeben...")                
                


                elif str(message_split[1]).lower() in tags_aktivit_reset:
                    last_activity_type = "none"
                    if online == True:
                        await client.change_presence(activity = None)
                    await message.author.send("Aktivität zurückgesetzt...")

                elif str(message_split[1]).lower() in tags_aktivit_game:
                    message_split.pop(0)
                    message_split.pop(0)
                    activity_content = " ".join(message_split)
                    if online == True:
                        await client.change_presence(activity = discord.Game(name = activity_content))
                    await message.author.send("Aktivität geändert...")
                    last_activity_content = activity_content
                    last_activity_type = "game"

                elif str(message_split[1]).lower() in tags_aktivit_movie:
                    message_split.pop(0)
                    message_split.pop(0)
                    activity_content = " ".join(message_split)
                    if online == True:
                        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_content))
                    await message.author.send("Aktivität geändert...")
                    last_activity_content = activity_content
                    last_activity_type = "movie"
                
                elif str(message_split[1]).lower() in tags_aktivit_music:
                    message_split.pop(0)
                    message_split.pop(0)
                    if str(message_split[-1]) == "zu":
                        message_split.pop(-1)
                    activity_content = " ".join(message_split)
                    if online == True:
                        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_content))
                    await message.author.send("Aktivität geändert...")
                    last_activity_content = activity_content
                    last_activity_type = "music"

                
                

            


        ## OP ENDE ##







    ## adminliste und gebannte und letzte aktivität speichern
    f = open("stuff.txt","w")

    f.write("admin: ")
    for i in range(len(admins)):
        f.write(admins[i] + " ")
    f.write("\n")

    f.write("not_authorized: ")
    for i in range(len(not_authorized)):
        f.write(not_authorized[i] + " ")
    f.write("\n")

    f.write("activities: ")
    f.write(last_activity_type + " ")
    if last_activity_type != "none":
        f.write(last_activity_content + " ")
    f.write("\n")
    
    f.write("prefix: ")
    f.write(prefix)
    f.write(" ")

    f.close()

    








## bot am laufen halten
keep_alive()


client.run(TOKEN)