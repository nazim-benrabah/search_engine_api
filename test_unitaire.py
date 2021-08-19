from requests import *

import unittest


class TestAPIMethods(unittest.TestCase):
    server_ip = "127.0.0.1"
    server_port = 8080

    def test_publications(self):
        r1 = get(f"http://{self.server_ip}:{self.server_port}/publications/10")
        
        self.assertEqual(r1.text,'Malware.')

    def test_pub_100(self):
        r2 = get(f"http://{self.server_ip}:{self.server_port}/publications")
        
        self.assertEqual(r2.text.split("</p>")[0], "<p>1 - Spectre Attacks: Exploiting Speculative Execution.")

    def test_pub_with_limit(self):
        r3 = get(f"http://{self.server_ip}:{self.server_port}/publications?limit=10")

        self.assertEqual(r3.text.split('</p>')[6],'<p>7 - Token.')

    def test_pub_of_author(self):
        r4 = get(f"http://{self.server_ip}:{self.server_port}/authors/Daniel Genkin/publications")
        
        self.assertEqual(r4.text,'<p> - Spectre Attacks: Exploiting Speculative Execution.</p><p> - Meltdown</p>')


    def test_info_author(self):
        r5 = get(f"http://{self.server_ip}:{self.server_port}/authors/Daniel Genkin")
        
        self.assertEqual(r5.text,'<p> le nombre de publication = 2 \n Le nombre de co-autheurs = 9</p>')

    def test_co_authors(self):
        r6 = get(f"http://{self.server_ip}:{self.server_port}/authors/Daniel Genkin/coauthors")
        

        self.assertEqual(r6.text,"['Paul Kocher', 'Daniel Gruss', 'Werner Haas 0004', 'Mike Hamburg', 'Moritz Lipp', 'Stefan Mangard', 'Thomas Prescher 0002', 'Michael Schwarz 0001', 'Yuval Yarom']")

    def test_co_authors_with_start_count(self):
        r7 = get(f"http://{self.server_ip}:{self.server_port}/authors/Paul Kocher/coauthors?start=1&count=3")
        

        self.assertEqual(r7.text,"['Daniel Gruss', 'Werner Haas 0004', 'Mike Hamburg', 'Moritz Lipp']")


    def test_search_author(self):

        r8 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/dANi")
        
    
        self.assertEqual(r8.text,"['Daniel Genkin', 'Daniel Gruss']")


    def test_search_author_with_start_count(self):

        r9 = get(f"http://{self.server_ip}:{self.server_port}/search/authors/p?start=1&count=3")
        
    
        self.assertEqual(r9.text,str(['Pierangela Samarati', 'Pete Forsyth', "Paidi O'Raghallaigh", 'Peter Van Roy']))



    def test_search_publication(self):
        r10 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/p")
        
        
        self.assertEqual(r10.text,str(['Privacy-Preserving Authentication in Wireless Access Networks.', 'Private Key Cryptosystem.', 'Public Key Proxy Signatures.', 'Pretty good anonymity: achieving high performance anonymity services with a single node architecture.', 'Proceedings of the 7th International Symposium on Wikis and Open Collaboration, 2011, Mountain View, CA, USA, October 3-5, 2011']))


    def test_search_publication_with_start_count(self):
        r11 = get(f"http://{self.server_ip}:{self.server_port}/search/publications/p?start=2&count=3")
        
        
        self.assertEqual(r11.text,str(['Public Key Proxy Signatures.', 'Pretty good anonymity: achieving high performance anonymity services with a single node architecture.', 'Proceedings of the 7th International Symposium on Wikis and Open Collaboration, 2011, Mountain View, CA, USA, October 3-5, 2011']))
    

    def test_distance(self):
        r12 = get(f"http://{self.server_ip}:{self.server_port}/authors/Paul Kocher/distance/Daniel Gruss")
        self.assertEqual(r12.text,str(1))

if __name__ == '__main__':
    unittest.main()