import discord
import json
import logging
import requests
from config import *

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.event
async def on_ready():
    print('{} Logged In!'.format(client.user.name))


@client.event
async def on_message(message):
    if message.content.startswith('!goat '):
        headers = {
            'User-Agent': user_agent
        }

        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.25.1',
            'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a',
            'x-algolia-application-id': '2FWOTDVM2O',
        }

        data = {
            "params": "query={}&facetFilters=(status%3Aactive%2C%20status%3Aactive_edit)%2C%20()&page=0&hitsPerPage=20".format(message.content.split('!goat ')[1])
        }

        response = requests.post(url=goat_url, headers=headers, params=params, json=data)
        output = json.loads(response.text)

        new_lowest_price_cents = int(output['hits'][0]['new_lowest_price_cents'] / 100)
        used_lowest_price_cents = int(output['hits'][0]['used_lowest_price_cents'] / 100)
        image = output['hits'][0]['picture_url']
        name = output['hits'][0]['name']
        url = 'https://www.goat.com/sneakers/' + output['hits'][0]['slug']

        embed = discord.Embed(color=000000)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Product Name", value="[{}]({})".format(name, url), inline=False)
        embed.add_field(name="New Lowest Price", value="${}".format(new_lowest_price_cents), inline=True)
        embed.add_field(name="Used Lowest Price", value="${}".format(used_lowest_price_cents), inline=True)

        await client.send_message(message.channel, embed=embed)


@client.event
async def on_message(message):
    if message.content.startswith('!stockx '):
        headers = {
            'User-Agent': user_agent
        }

        params = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
            'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
            'x-algolia-application-id': 'XW7SBCT9V6',
        }

        data = {
            "params": "query={}&hitsPerPage=20&facets=*".format(message.content.split('!stockx ')[1])
        }

        response = requests.post(url=stockx_url, headers=headers, params=params, json=data)
        output = json.loads(response.text)

        deadstock_sold = output['hits'][0]['deadstock_sold']
        highest_ask = output['facets_stats']['lowest_ask']['max']
        highest_bid = output['hits'][0]['highest_bid']
        image = output['hits'][0]['media']['imageUrl']
        last_sale = output['hits'][0]['last_sale']
        lowest_ask = output['hits'][0]['lowest_ask']
        name = output['hits'][0]['name']
        sales_last_72 = output['hits'][0]['sales_last_72']
        url = 'https://stockx.com/' + output['hits'][0]['url']

        embed = discord.Embed(color=4500277)
        embed.set_thumbnail(url=image)
        embed.add_field(name="Product Name", value="[{}]({})".format(name, url), inline=False)
        embed.add_field(name="Last Sale", value="${}".format(last_sale), inline=True)
        embed.add_field(name="Highest Bid", value="${}".format(highest_bid), inline=True)
        embed.add_field(name="Lowest Ask", value="${}".format(lowest_ask), inline=True)
        embed.add_field(name="Highest Ask", value="${}".format(highest_ask), inline=True)
        embed.add_field(name="Units Sold in Last 72 Hrs", value="{}".format(sales_last_72), inline=True)
        embed.add_field(name="Total Units Sold", value="{}".format(deadstock_sold), inline=True)

        await client.send_message(message.channel, embed=embed)


client.run(token)
