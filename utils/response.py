from discord import ApplicationContext, Colour, Embed

async def success_embed(ctx: ApplicationContext, action, title=None):
    return await ctx.respond(
        embed = Embed(
            title=title,
            description=f"<:jaxie_done:1043740363803865089> Successfully {action}",
            color=Colour.magenta()
        ).set_footer(
            text=f"Action performed by {ctx.author.name}"
        )
    )
