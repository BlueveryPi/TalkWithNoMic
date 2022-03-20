import discord, asyncio, aiohttp, os
from discord.ext import commands

token=
game=discord.Game("테스트중")
intents = discord.Intents().all()
ffmpeg_options = {"options": "-vn"}
bot=commands.Bot(command_prefix="!", status=discord.Status.online, activity=game, intents=intents, help_command=None)

KEY=

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, volume=1):
        super().__init__(source, volume)
        self.id=None

    @classmethod
    async def from_url(self, filename):
        return self(discord.FFmpegPCMAudio(filename, **ffmpeg_options))

async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("아무런 음성채널에도 접속해 계시지 않네요.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()


@bot.event
async def on_ready():
    print("ready!")

def after(e):
    if e is not None:
        print(e)
    else:
        os.remove(f"./codes/botify/{YTDLSource.id}.mp3")

@bot.before_invoke(ensure_voice)
@bot.slash_command(guild_id=[851650387039617035, 851650387039617035])
async def 채터(ctx:discord.ApplicationContext, text: discord.Option(str, "무슨 말을 할까요?"), voice: discord.Option(str, choices=["WOMAN_READ_CALM", "MAN_READ_CALM", "WOMAN_DIALOG_BRIGHT", "MAN_DIALOG_BRIGHT"])="MAN_DIALOG_BRIGHT"):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://kakaoi-newtone-openapi.kakao.com/v1/synthesize', headers={"Content-Type": "application/xml", "Authorization": f"KakaoAK {KEY}"}, data=f'<speak><voice name=\"{voice}\"> {text}</voice></speak>') as response:
            with open(f"./codes/botify/{ctx.user.id}.mp3", "wb") as f:
                f.write(await response.read())
            YTDLSource.id=ctx.user.id
            player = await YTDLSource.from_url(f"./codes/botify/{ctx.user.id}.mp3")
            ctx.voice_client.play(player, after=after)
            await ctx.respond("전송 완료!")
            await asyncio.sleep(3)
            await ctx.delete()

bot.run(token)