from src.ETL.extract import ExtractSpotify
from src.utils.search import Search
class Main: 
    def __init__(self):
        pass
    
    def run(self):
        e = Search()
        e.SearchTracksPop()
        
        
main = Main()
main.run()