from discord import ApplicationContext, Colour, Embed, Interaction

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

async def forbidden_error_embed(interaction: Interaction, action: str, permission: str):
    return await interaction.response.send_message(
        embed = Embed(
            description=f"<:jaxie_mad:1043740361052393542> I am lacking the permission `{permission}` to {action}.\nKindly grant me the permission to proceed.",
            color=Colour.red()
        ),
        ephemeral=True
    )

async def missingperms_error_embed(interaction: Interaction, permission: str, action: str):
    return await interaction.response.send_message(
        embed = Embed(
            description=f"<:jaxie_stop:1043741515563937873> You lack the permission `{permission}` to {action}.",
            color=Colour.red()
        ),
        ephemeral=True
    )
