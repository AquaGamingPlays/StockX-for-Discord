import json

import discord
import requests


with open('config.json') as json_file:
    config = json.load(json_file)

discord_token = config['discord_token']
api_url = config['api_url']
base_url = config['base_url']

client = discord.Client()


@client.event
async def on_ready():
    print('{} Logged In!'.format(client.user.name))


@client.event
async def on_message(message):
    if message.content.startswith('!stockx '):
        product_name = message.content.split('!stockx ')[1]

        payload = {
            'x-algolia-agent': 'Algolia for vanilla JavaScript 3.27.1',
            'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
            'x-algolia-application-id': 'XW7SBCT9V6'
        }

        json_payload = {
            "params": "query={}&hitsPerPage=1".format(product_name)
        }

        r = requests.post(url=api_url, params=payload, json=json_payload)
        output = json.loads(r.text)

        name = output['hits'][0]['name']
        thumbnail_url = output['hits'][0]['thumbnail_url']
        url = base_url + output['hits'][0]['url']
        release_date = output['hits'][0]['release_date']
        style_id = output['hits'][0]['style_id']
        highest_bid = output['hits'][0]['highest_bid']
        lowest_ask = output['hits'][0]['lowest_ask']
        last_sale = output['hits'][0]['last_sale']
        sales_last_72 = output['hits'][0]['sales_last_72']
        deadstock_sold = output['hits'][0]['deadstock_sold']
        retail_price = output['hits'][0]['searchable_traits']['Retail Price']

        embed = discord.Embed(color=4500277)
        embed.set_thumbnail(url=thumbnail_url)
        embed.add_field(name='Product Name', value='[{}]({})'.format(name, url), inline=False)
        embed.add_field(name='Style ID', value = '{}'.format(style_id), inline=True)
        embed.add_field(name='Release Date', value='{}'.format(release_date), inline=True)
        embed.add_field(name='Retail Price', value='${}'.format(retail_price), inline=True)
        embed.add_field(name='Last Sale', value='${}'.format(last_sale), inline=True)
        embed.add_field(name='Lowest Ask', value='${}'.format(lowest_ask), inline=True)
        embed.add_field(name='Highest Bid', value='${}'.format(highest_bid), inline=True)
        embed.add_field(name='Units Sold in Last 3 Days', value='{}'.format(sales_last_72), inline=True)
        embed.add_field(name='Total Units Sold', value='{}'.format(deadstock_sold), inline=True)

        await client.send_message(message.channel, embed=embed)


client.run(discord_token)
