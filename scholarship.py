from webdriver_manager.chrome import ChromeDriverManager # another doc need
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from typing import List
import re

opts = webdriver.ChromeOptions()
opts.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)




class Scholarship:
    def __init__(self) -> None:
        self.home_site = "https://www.scholarshipscanada.com/Index.aspx"
        self.home_page = urlopen(self.home_site)
        self.home_html = self.home_page.read().decode("utf-8")
        self.soup = BeautifulSoup(self.home_html, "html.parser")

        self.scholarship_links = self._get_links()
        # print(self.scholarship_links)
        self.ordered_scholarship_set_3x5 = [
            [self.scholarship_links[link] for link in range(5)],
            [self.scholarship_links[link] for link in range(5, 10)],
            [self.scholarship_links[link] for link in range(10, 15)]
        ]

        self.asd = list(re.findall('Scholarships/.*?/', _) for _ in self.scholarship_links)
        self.scholarship_names = [
            self.scholarship_links[it][self.scholarship_links[it].find(self.asd[it][0]) + len(self.asd[it][0]):].replace('-', ' ') 
            for it in range(15)
        ]
        
        
        

    def _find_part_size(self, to_find: int) -> int:
        """find site width or height"""

        return driver.execute_script("return document.body.parentNode.scroll" + to_find)




    def _get_links(self) -> List[str]:
        """gets scholarship links, cleans them, and sends them back"""

        link_section_html = self.soup.find_all("a", class_='bold')
        # all 15 raw links (still has href=..., quotes, etc - used to find with rgx)
        # findall creates lists within unedited_links: a list 
        unedited_links = [re.findall('href="/Scholarships/.*?"', str(html_to_use)) 
                          for html_to_use in link_section_html
                    ]
        # removes useless stuff
        return [f"https://www.scholarshipscanada.com{finished_link[0][6 : -1]}" for finished_link in unedited_links]




    def get_site_info(self, site: str) -> List[int]:
        """take the pictures and send back a list to be used as an iterator taking the place
        of the number of pictures being screenshotted and sent, which will always be three"""

        driver.get(site)
        driver.set_window_size(self._find_part_size("Width"), self._find_part_size("Height"))

        # these are the three main parts needed to understand the scholarship page
        driver.find_element_by_xpath("//div[@class='Primary-Info-Wrapper']").screenshot('scholp1.png'),
        driver.find_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder1_pnlScholarshipNotes']").screenshot('scholp2.png'),
        driver.find_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder1_pnlDetails']").screenshot('scholp3.png'),
        # sends useless list to be iterated with later when finding the pictures. also reduces code
        return [_ for _ in range(3)]
    
