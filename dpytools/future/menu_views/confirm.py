import discord
from discord import ui, Interaction

from ..utils import randstr

__all__ = (
    'Confirm',
)

class _ConfirmButton(ui.Button):
    def __init__(self, label, val, view):
        self.val = val
        self._view = view
        style = discord.ButtonStyle.green if self.val \
            else discord.ButtonStyle.gray
        custom_id = f'{randstr(10)}:{label.lower()}'
        super().__init__(label=label, style=style, custom_id=custom_id)

    async def callback(self, interaction: Interaction):
        return await self._view.ack(interaction, self.val)


class Confirm(discord.ui.View):
    """
    Classic confirm view with two buttons.

    Parameters
    ----------
        confirm_label: the label for the confirm button
        cancel_label: the label for the cancel button
        *args/**kwargs: see discord.ui.View params

    Behaviour::

        When the view is displayed it will await for a button press
        When the button is pressed the inner :value: attribute will be set
            if confirmed: to True
            if cancelled: to False
        If timeout is specified and reached value will be None.

        If the view timeouts, gets an error or finishes by buttonpress
        buttons will be disabled

    """
    def __init__(self, *args, confirm_label='Confirm', cancel_label='Cancel', **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None
        self.msg = None
        self.add_item(_ConfirmButton(confirm_label, True, self))
        self.add_item(_ConfirmButton(cancel_label, False, self))

    async def ack(self, inter, value):
        await inter.response.defer()
        self.msg = inter.message
        self.value = value
        await self.disable()
        self.stop()

    async def disable(self):
        if self.msg:
            for btn in self.children:
                btn.disabled = True
            await self.msg.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable()
