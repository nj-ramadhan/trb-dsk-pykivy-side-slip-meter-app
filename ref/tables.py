from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen


class Example(MDApp):
    def build(self):
        self.data_tables = MDDataTable(
            use_pagination=True,
            check=True,
            column_data=[
                ("No.", dp(30)),
                ("Status", dp(30)),
                ("Signal Name", dp(60)),
                ("Severity", dp(30)),
                ("Stage", dp(30)),
                ("Schedule", dp(30)),
                ("Team Lead", dp(30)),
            ],
            row_data=[
                (
                    "0",
                    ("alert", [255 / 256, 165 / 256, 0, 1], "No Signal"),
                    "Astrid: NE shared managed",
                    "Medium",
                    "Triaged",
                    "0:33",
                    "Chase Nguyen",
                ),
                (
                    "1",
                    ("alert-circle", [1, 0, 0, 1], "Offline"),
                    "Cosmo: prod shared ares",
                    "Huge",
                    "Triaged",
                    "0:39",
                    "Brie Furman",
                ),
                (
                    "2",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Phoenix: prod shared lyra-lists",
                    "Minor",
                    "Not Triaged",
                    "3:12",
                    "Jeremy lake",
                ),
                (
                    "3",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Sirius: NW prod shared locations",
                    "Negligible",
                    "Triaged",
                    "13:18",
                    "Angelica Howards",
                ),
                (
                    "4",
                    (
                        "checkbox-marked-circle",
                        [39 / 256, 174 / 256, 96 / 256, 1],
                        "Online",
                    ),
                    "Sirius: prod independent account",
                    "Negligible",
                    "Triaged",
                    "22:06",
                    "Diane Okuma",
                ),
            ],
            sorted_on="Schedule",
            sorted_order="ASC",
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        self.data_tables.bind(on_check_press=self.on_check_press)
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def on_row_press(self, table, row):
        '''Called when a table row is clicked.'''

        print(table, row)

        # Using the first value as index. There should be some more proper way to do that
        # but this is just to show the issue

        start_index, end_index  = row.table.recycle_data[row.index]["range"]
        value1                  = int(row.table.recycle_data[start_index]["text"])

        value2                  = row.table.recycle_data[2]["text"]

        print("value1 %d" % value1)

        one_item =        (
            value1,
            (
                "alert",
                [256 / 256, 174 / 256, 0 / 256, 1],
                "Online",
                ),
            "Somethine else !",
            "Something differnt",
            "Triaged",
            "22:06",
            "Me Me me",
        )

        table.update_row(self.data_tables.row_data[value1], one_item)

    def on_check_press(self, instance_table, current_row):
        '''Called when the check box in the table row is checked.'''

        print(instance_table, current_row)

Example().run()