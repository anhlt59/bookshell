from typing import Iterator

from rich import box
from rich.console import Console as RichConsole
from rich.live import Live
from rich.table import Table


class LiveType:
    UPDATE = 0
    INSERT = 1


class Console(RichConsole):
    @staticmethod
    def generate_table(items: list[list], columns: list[str] = None) -> Table:
        """Make a new table."""
        table = Table(box=box.SIMPLE)
        for column in columns:
            table.add_column(**column)

        for item in items:
            table.add_row(*item)
        return table

    def show_table(self, items: list[list], columns: list[str] = None):
        """Show rich table."""
        if items:
            table = self.generate_table(items, columns)
            self.print(table)
        else:
            self.log("No items found", style="yellow")

    def live_table(
        self,
        chunk_items: Iterator[list],
        columns: list[str] = None,
        live_type: str = LiveType.UPDATE,
        refresh_per_second: int = 1,
    ):
        """Show live table."""
        table = self.generate_table([], columns)

        with Live(table, refresh_per_second=refresh_per_second) as live:
            for items in chunk_items:
                if live_type == LiveType.INSERT:
                    table.add_row(*items)
                elif live_type == LiveType.UPDATE:
                    live.update(self.generate_table(items, columns))
                else:
                    raise ValueError(f"Invalid live_type: {live_type}")


console = Console()
