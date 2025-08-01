from nicegui import run, ui
from nicegui.elements.spinner import SpinnerTypes


class LoadingSpinnerModal(ui.dialog):
    def __init__(
        self,
        *,
        spinner_type: SpinnerTypes = "default",
        spinner_size: str = "10em",
        spinner_color: str = "primary",
        spinner_thickness: float = 5,
    ) -> None:
        """Loading modal screen.

        Add this element to the top of the page and use `loading_while` function to generate a loading screen
        while the function executes.

        Example: `lambda e: loading_modal.loading_while(asyncio.sleep, delay=15)` where delay is a parameter for sleep.
        loading_modal is the name of the variable of this class instance.


        Some good looking spinners: audio, bars, box, dots, hourglass, puff

        Args:
            spinner_type (SpinnerTypes, optional): Type of spinner. Defaults to "default".
            spinner_size (str, optional): Size of spinner. Defaults to "10em".
            spinner_color (str, optional): Color of spinner (uses Tailwind CSS color notation). Defaults to "primary".
            spinner_thickness (float, optional): Thickness of the spinner. Defaults to 5.
        """
        super().__init__(value=False)
        self.props("persistent backdrop-filter='blur(5px)'")

        with self:
            ui.spinner(
                spinner_type,
                size=spinner_size,
                color=spinner_color,
                thickness=spinner_thickness,
            )

    async def loading_while(self, async_function=None, **kwargs):
        """Function to start and stop loading screen for the duratin of a function.

        Example: `lambda e: loadingDialog.loading_while(asyncio.sleep, delay=15)` where delay is a parameter for sleep

        Args:
            async_function (optional): Async function (should not be called) with its arguments passed as kwargs. Defaults to None.

        """
        result = None

        self.open()
        if async_function is not None:
            result = await async_function(**kwargs)
        self.close()

        return result

    async def loading_while2(self, non_async_function=None, **kwargs):
        """Function to start and stop loading screen for the duratin of a function.

        Args:
            async_function (optional): Async function (should not be called) with its arguments passed as kwargs. Defaults to None.

            Example: `lambda e: loadingDialog.loading_while(asyncio.sleep, delay=15)` where delay is a parameter for sleep
        """
        result = None

        self.open()
        if non_async_function is not None:
            result = await run.io_bound(non_async_function, **kwargs)
        self.close()

        return result
