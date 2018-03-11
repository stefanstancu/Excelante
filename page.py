from datetime import datetime as dt
import re

from statemap import state_map

class Page:
    date_format = "%m/%d/%Y"

    def __init__(self, raw_text):
        self.raw_text = raw_text

        # Dates
        dates = re.split(": | - ", self.raw_text[0])
        self.start_date = dt.strptime(dates[1], self.date_format)
        self.end_date = dt.strptime(dates[2], self.date_format)

        # State Name
        self.state = state_map[self.raw_text[1].strip()]

        # Rating Group
        self.rating = int(self.raw_text[2].split(":")[1][4:-1]);

        # Plan Name
        self.product_name = self.raw_text[3].split(":")[-1][1:]

        # Data
        self._scrape_data()

    def print_page(self):
        print("Date Range: " + str(self.start_date) + " : " + str(self.end_date))
        print("State: " + self.state)
        print("Rating Group: " + str(self.rating))
        print("Plan Name: " + self.product_name)

        for key, value in self.data.items():
            print("    " + key + ": " + str(value))
    
    def data_list(self):
        """
        Return data as a list in the order needed to print the data
        """
        data_list = []
        for i in range(21, 65):
            data_list.insert(i - 18, self.data[str(i)])

        data_list.insert(0, self.data["0-18"])
        data_list.insert(1, self.data["19-20"])
        data_list.append(self.data["65+"])
        
        return data_list


    def _scrape_data(self):
        # The desired output has ranges 0-18 and 19-20 which in the pdfs are available as 0-20.
        # The same occurs with range 64. The pdf only contains 64+.
        # The missing data range will assume a value from the the available pdf data
        #   i.e. 0-18 and 19-20 will have the value in pdf range of 0-20
        self.data = {}
        for line in self.raw_text[5:]:
            temp = line.split()
            for i in [0, 2, 4]:
                self.data[temp[i]] = float(temp[i+1])

        self.data["0-18"] = self.data["0-20"]
        self.data["19-20"] = self.data["0-20"]
        self.data["64"] = self.data["64+"]
        self.data["65+"] = self.data["64+"]

        del self.data["0-20"]
        del self.data["64+"]

