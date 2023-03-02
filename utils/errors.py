from discord import ApplicationContext, Colour, Embed


async def http_error(ctx: ApplicationContext):
    await ctx.respond(
        embed = Embed(
            title="<:jaxie_mad:1043740361052393542> Unable to perform this action due to an error with discord.",
            color=Colour.red()
        )
    )

async def hierarchy_error(ctx: ApplicationContext, mode):
    await ctx.respond(
        embed = Embed(
            title=f"<:jaxie_mad:1043740361052393542> Unable to {mode}",
            description=f"Make sure you are above the person to be {mode}ed and so am I in terms of Discord hierarchy.",
            color=Colour.red()
        )
    )

async def permission_error(ctx: ApplicationContext, mode):
    await ctx.respond(
        embed = Embed(
            title=f"<:jaxie_stop:1043741515563937873> Unable to {mode}",
            description="Make sure you/I have enough permissions to perform this action.",
            color=Colour.red()
        )
    )
