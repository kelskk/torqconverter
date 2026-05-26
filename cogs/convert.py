import discord

from discord.ext import commands
from discord import app_commands

import uuid
import os
import yt_dlp

from utils.downloader import download_file
from utils.converter import convert_file
from utils.cleanup import cleanup


class Convert(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ==========================
    # /CONVERT
    # ==========================

    @app_commands.command(
        name="convert",
        description="Converter arquivos"
    )

    @app_commands.describe(
        to="Formato",
        link="Link",
        arquivo="Arquivo"
    )

    async def convert(

        self,

        interaction: discord.Interaction,

        to: str,

        link: str = None,

        arquivo: discord.Attachment = None

    ):

        await interaction.response.defer()

        uid = str(
            uuid.uuid4()
        )

        input_path = (
            f"temp/{uid}_input"
        )

        output_path = (
            f"temp/{uid}.{to}"
        )

        try:

            if arquivo:

                await arquivo.save(
                    input_path
                )

            elif link:

                download_file(
                    link,
                    input_path
                )

            else:

                return await interaction.followup.send(
                    "Envie arquivo ou link"
                )

            convert_file(
                input_path,
                output_path,
                to
            )

            await interaction.followup.send(

                file=
                discord.File(
                    output_path
                )

            )

        except Exception as e:

            await interaction.followup.send(
                f"❌ {e}"
            )

        finally:

            cleanup(
                input_path,
                output_path
            )

    # ==========================
    # /DOWNLOAD
    # ==========================

    @app_commands.command(
        name="download",
        description="Baixar vídeo ou música"
    )

    @app_commands.describe(

        link="URL",

        formato=
        "mp3 mp4 wav webm mkv m4a"

    )

    async def download(

        self,

        interaction: discord.Interaction,

        link: str,

        formato: str

    ):

        await interaction.response.defer()

        formato = formato.lower()

        PERMITIDOS = [

            "mp3",
            "wav",
            "m4a",

            "mp4",
            "webm",
            "mkv"

        ]

        if formato not in PERMITIDOS:

            return await interaction.followup.send(

                "❌ Apenas áudio/vídeo"

            )

        uid = str(
            uuid.uuid4()
        )

        output = (
            f"temp/{uid}.%(ext)s"
        )

        arquivo = None

        try:

            opts = {

                "outtmpl":
                output,

                "quiet":
                True,

                "noplaylist":
                True

            }

            if formato in [

                "mp3",
                "wav",
                "m4a"

            ]:

                opts.update({

                    "format":
                    "bestaudio",

                    "postprocessors": [

                        {

                            "key":
                            "FFmpegExtractAudio",

                            "preferredcodec":
                            formato

                        }

                    ]

                })

            else:

                opts.update({

                    "format":
                    "bestvideo+bestaudio/best"

                })

            url_final = link

            # Spotify
            if "spotify.com" in link:

                sp_opts = {
                    "quiet": True
                }

                with yt_dlp.YoutubeDL(
                    sp_opts
                ) as sp:

                    info = sp.extract_info(
                        link,
                        download=False
                    )

                nome = (

                    info.get(
                        "track"
                    )

                    or

                    info.get(
                        "title"
                    )

                )

                artista = (

                    info.get(
                        "artist"
                    )

                    or ""

                )

                busca = (
                    f"ytsearch1:{nome} {artista}"
                )

                url_final = busca

            with yt_dlp.YoutubeDL(
                opts
            ) as ydl:

                ydl.download(
                    [url_final]
                )

            for f in os.listdir(
                "temp"
            ):

                if uid in f:

                    arquivo = os.path.join(
                        "temp",
                        f
                    )

                    break

            if not arquivo:

                raise Exception(
                    "Download falhou"
                )

            await interaction.followup.send(

                content=
                f"✅ {formato}",

                file=
                discord.File(
                    arquivo
                )

            )

        except Exception as e:

            await interaction.followup.send(
                f"❌ {e}"
            )

        finally:

            if arquivo:

                cleanup(
                    arquivo
                )


async def setup(bot):

    await bot.add_cog(
        Convert(bot)
    )
