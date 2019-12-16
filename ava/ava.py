from datetime import datetime

import discord
import os
import random
import pkg_resources
from discord.ext import commands
import asyncio
import aiml
import logging
import logging.config
import sqlite3
import cv2
import urllib
from ava.utils.crawler import *

import hashlib

STARTUP_FILE = "std-startup.xml"
DEFAULT_PROPS = "bot.properties"
BOT_PREFIX = ('?', '!')
SQL_SCHEMA = """CREATE TABLE IF NOT EXISTS
chat_log (time, server_name, user_id, message, response)"""
SQL_SCHEMA_2 = """CREATE TABLE IF NOT EXISTS
users (id, name, first_seen)"""
SQL_SCHEMA_3 = """CREATE TABLE IF NOT EXISTS
servers (id, name, first_seen)"""

class Ava:

    def __init__(self, channel_name, bot_token, log_file, database):
        self.log_file = log_file
        self.database = database

        # Log configuration
        self.logger = logging.getLogger('cathy_logger')
        self.setup_logging()
        self.logger.info("[+] Initialized logging for bot.")
        self.cache = load_dict_from_file()
        # Setup database
        self.db = sqlite3.connect(self.database)
        self.cursor = self.db.cursor()
        self.setup_database_schema()

        # Load AIML kernel
        self.logger.info("[*] Initializing AIML kernel...")
        self.aiml_kernel = aiml.Kernel()
        initial_dir = os.getcwd()
        os.chdir(pkg_resources.resource_filename(__name__, ''))  # Change directories to load AIML files properly
        startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
        self.aiml_kernel.learn(startup_filename)

        properties_file = open(os.sep.join([os.getcwd(), DEFAULT_PROPS]))
        for line in properties_file:
            parts = line.split('=')
            key = parts[0]
            value = parts[1]
            self.aiml_kernel.setBotPredicate(key, value)

        self.aiml_kernel.respond("LOAD AIML B")
        os.chdir(initial_dir)
        self.logger.info("[+] Done initializing AIML kernel.")

        # Set up Discord
        self.logger.info("[*] Initializing Discord bot...")
        self.channel_name = channel_name
        self.token = bot_token
        self.discord_client = commands.Bot(command_prefix=BOT_PREFIX)
        self.setup_discord_events()
        self.logger.info("[+] Done initializing Discord bot.")


    def setup_logging(self):
        self.logger.setLevel(logging.INFO)
        log_file_handler = logging.FileHandler(self.log_file)
        log_file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
        log_file_handler.setFormatter(formatter)
        self.logger.addHandler(log_file_handler)

    def setup_database_schema(self):
        self.cursor.execute(SQL_SCHEMA)
        self.cursor.execute(SQL_SCHEMA_2)
        self.cursor.execute(SQL_SCHEMA_3)
        self.db.commit()

    def setup_discord_events(self):

        @self.discord_client.event
        @asyncio.coroutine
        def on_ready():
            self.logger.info("[+] Bot connected to Discord")
            self.logger.info("[*] Name: {}".format(self.discord_client.user.name))
            self.logger.info("[*] ID: {}".format(self.discord_client.user.id))
            yield from self.discord_client.change_presence(game=discord.Game(name='Developed by Giriprak(Ash)'))

        @self.discord_client.event
        @asyncio.coroutine
        def on_message(message):
            if message.author.bot or (not str(message.channel).__contains__(self.channel_name)
            and not str(message.channel).__contains__('whos-that-pokemon')):
                return
            elif message.content is None:
                self.logger.error("[-] Empty message received.")
                return
            elif (not message.author.bot) and str(message.channel).__contains__('whos-that-pokemon'):
                str_content = str(message.content)
                if "cdn" not in str_content and "discord" not in str_content and "attachments" not in str_content:
                    # print("invalid url")
                    return
                else:
                    poke_url = str_content
                    self.current_url = poke_url
                    # print("valid image")
                    img_bytes = self.get_img_bytes(poke_url)
                    img_hash = hashlib.sha3_256(img_bytes).hexdigest()
                    # print(img_hash)
                    if img_hash in self.cache:
                        # print("Pokemon data found in cache!")
                        text = self.cache[img_hash]
                        # print(text)
                        yield from self.discord_client.send_message(message.channel, text)
                        return
                    response_list = get_pokemon(self.current_url)
                    print(response_list)
                    yield from self.discord_client.send_message(message.channel, "Sorry, I don't know this pokemon. :(")
                    yield from self.discord_client.send_message(message.channel, response_list)
                    return
            elif (not message.author.bot) and str(message.channel).__contains__(self.channel_name):
                now = datetime.now()
                try:
                    aiml_response = self.aiml_kernel.respond(message.content)
                    aiml_response = aiml_response.replace("://", "")
                    aiml_response = "%s: %s" % (message.author.mention, aiml_response)

                    self.logger.info("[%s] (%s) %s: %s\nResponse: %s" %
                                     (now.isoformat(), message.server.name, message.author, message.content, aiml_response))
                    self.insert_chat_log(now, message, aiml_response)

                    yield from self.discord_client.send_typing(message.channel)
                    yield from asyncio.sleep(random.randint(1, 3))
                    yield from self.discord_client.send_message(message.channel, aiml_response)

                except discord.HTTPException as e:
                    self.logger.error("[-] Discord HTTP Error: %s" % e)
                except Exception as e:
                    self.logger.error("[-] General Error: %s" % e)

    def run(self):
        self.logger.info("[*] Attempting to run bot...")
        self.discord_client.run(self.token)
        self.logger.info("[*] Bot run.")

    def get_img_bytes(self, url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        image_name = "temp.jpg"
        urllib.request.urlretrieve(url, image_name)
        try:
            # img = cv2.imread(image_name,
            #                  cv2.IMREAD_GRAYSCALE)
            # resized_image = cv2.resize(img, (100, 100))
            # img_str = cv2.imencode('.png', resized_image)[1].tostring()
            img = cv2.imread(image_name)
            img_str = cv2.imencode('.png', img)[1].tostring()
        except Exception as e:
            print(str(e))
        try:
            os.remove(image_name)
        except: pass
        return img_str

    def insert_chat_log(self, now, message, aiml_response):
        self.cursor.execute('INSERT INTO chat_log VALUES (?, ?, ?, ?, ?)',
                            (now.isoformat(), message.server.id, message.author.id,
                                str(message.content), aiml_response))

        # Add user if necessary
        self.cursor.execute('SELECT id FROM users WHERE id=?', (message.author.id,))
        if not self.cursor.fetchone():
            self.cursor.execute(
                'INSERT INTO users VALUES (?, ?, ?)',
                (message.author.id, message.author.name, datetime.now().isoformat()))

        # Add server if necessary
        self.cursor.execute('SELECT id FROM servers WHERE id=?', (message.server.id,))
        if not self.cursor.fetchone():
            self.cursor.execute(
                'INSERT INTO servers VALUES (?, ?, ?)',
                (message.server.id, message.server.name, datetime.now().isoformat()))

        self.db.commit()



