from copy import copy
from time import perf_counter

from discord import Message
from discord.ext import commands


class TimedCommands(commands.Cog):
    """Time the command execution of a command."""

    @staticmethod
    async def create_execution_context(ctx: commands.Context, command: str) -> commands.Context:
        """Get a new execution context for a command."""
        msg: Message = copy(ctx.message)
        msg._update({"content": f"{ctx.prefix}{command}"})

        return await ctx.bot.get_context(msg)

    @commands.command(name="timed", aliases=["t"])
    async def timed(self, ctx: commands.Context, *, command: str) -> None:
        """Time the command execution of a command."""
        new_ctx = await self.create_execution_context(ctx, command)

        if new_ctx.command and new_ctx.command.qualified_name == "timed":
            return await ctx.send("You are not allowed to time the execution of the `timed` command.")

        t_start = perf_counter()
        await new_ctx.command.invoke(new_ctx)
        t_end = perf_counter()

        await ctx.send(f"Command execution for `{new_ctx.command}` finished in {(t_end - t_start):.4f} seconds.")


def setup(bot: commands.Bot) -> None:
    """Cog load."""
    bot.add_cog(TimedCommands(bot))
