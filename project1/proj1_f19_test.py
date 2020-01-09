import unittest
import json
import proj1_f19 as proj1
from proj1_f19 import get_API_stuff


class TestMedia(unittest.TestCase):

    def testConstructor(self):
        m1 = proj1.Media()
        m2 = proj1.Media("1999", "Prince")
        m3 = proj1.Media("A Thousand Miles", "Vanessa Carlton", "2002")

        self.assertEqual(m1.title, "No Title")
        self.assertEqual(m1.author, "No Author")
        self.assertEqual(m2.title, "1999")
        self.assertEqual(m2.author, "Prince")
        self.assertEqual(m3.title, "A Thousand Miles")
        self.assertEqual(m3.author, "Vanessa Carlton")
        self.assertEqual(m3.releaseyear, "2002")
        self.assertEqual(len(m2), 0)
        self.assertEqual(len(m3), 0)
        print(m1)
        print(m2)
        print(m3)

    def testSong(self):
        s2 = proj1.Song("A Team", "Ed Sheeran", "2011", "+", "pop", "3600.00")
        s1 = proj1.Song()
        self.assertEqual(s2.title, "A Team")
        self.assertEqual(s2.author, "Ed Sheeran")
        self.assertEqual(s2.releaseyear, "2011")
        self.assertEqual(s2.album, "+")
        self.assertEqual(s2.genre, "pop")
        self.assertEqual(s2.tracklength, "3600.00")
        self.assertEqual(len(s2), 60)
        self.assertEqual(s1.title, "No Title")
        self.assertEqual(s1.album, "No Album")
        self.assertEqual(s1.tracklength, "No Length")
        self.assertEqual(s1.genre, "No Genre")
        print(s1)
        print(s2)
    
    def testMovie(self):
        mov1 = proj1.Movie("Avengers", "idk", "2010", "9", "48982.00")
        mov2 = proj1.Movie()
        self.assertEqual(mov1.title, "Avengers")
        self.assertEqual(mov1.author, "idk")
        self.assertEqual(mov1.releaseyear, "2010")
        self.assertEqual(mov1.rating, "9")
        self.assertEqual(mov1.movielength, "48982.00")
        self.assertEqual(len(mov1), 14)
        self.assertEqual(mov2.rating, "No Rating")
        self.assertEqual(mov2.movielength, "No Length")
        print(mov2)
        print(mov1)

class part2Test(unittest.TestCase):

    def testMediaJson(self):
        with open ('sample_json.json', 'r') as j:
            file = json.load(j)
        me1 = proj1.Media(jsonDict=file[0])
        self.assertEqual(me1.title, "Jaws")
        self.assertEqual(me1.author, "Steven Spielberg")
        self.assertEqual(me1.releaseyear, "1975")
        self.assertEqual(len(me1), 0)
        print(me1)
    
    def testSongJson(self):
        with open ('sample_json.json', 'r') as j:
            file = json.load(j)
        
        song1 = proj1.Song(jsonDict=file[1])
        self.assertEqual(song1.title, "Hey Jude")
        self.assertEqual(song1.author, "The Beatles")
        self.assertEqual(song1.releaseyear, "1968")
        self.assertEqual(song1.album, "TheBeatles 1967-1970 (The Blue Album)")
        self.assertEqual(song1.genre, "Rock")
        self.assertEqual(song1.tracklength, 431333)
        self.assertEqual(len(song1), 7189.00)
        print(song1)

    def testMovieJson(self):
        with open ('sample_json.json', 'r') as j:
            file = json.load(j)
        movie1 = proj1.Movie(jsonDict=file[0])
        self.assertEqual(movie1.title, "Jaws")
        self.assertEqual(movie1.author, "Steven Spielberg")
        self.assertEqual(movie1.releaseyear, "1975")
        self.assertEqual(movie1.rating, "PG")
        self.assertEqual(movie1.movielength, 7451455)
        self.assertEqual(len(movie1), 2070.0)
        print(movie1)

class part3Test(unittest.TestCase):
    def testAPI(self):
        instance = get_API_stuff("Taylor Swift", 5)
        tswift1 = proj1.Song(jsonDict=instance[0])
        print(tswift1)
        tswift2 = proj1.Song(jsonDict=instance[1])
        print(tswift2)
        tswift3 = proj1.Song(jsonDict=instance[2])
        print(tswift3)
        tswift4 = proj1.Song(jsonDict=instance[3])
        print(tswift4)
        tswift5 = proj1.Song(jsonDict=instance[4])
        print(tswift5)
        print(len(instance))

        instance2 = get_API_stuff("moana", 3)
        moana1 = proj1.Movie(jsonDict=instance2[1])
        print(moana1)
        moana2 = proj1.Song(jsonDict=instance2[0])
        print(moana2)
        moana3 = proj1.Media(jsonDict=instance2[2])
        print(moana3)
        print(len(instance2))

        instance3 = get_API_stuff("baby", 5)
        print(len(instance3))

        instance4 = get_API_stuff("", "")
        print(len(instance4))

        instance5 = get_API_stuff("&@#!$")
        print(len(instance5))
        gibberish = proj1.Media(jsonDict=instance5[0])
        print(gibberish)
        
        instance6 = get_API_stuff("helter skelter")
        print(len(instance6))
        helter = proj1.Media(jsonDict=instance6[0])
        print(helter)
        
        instance7 = get_API_stuff("love")
        print(len(instance7))
        love = proj1.Media(jsonDict=instance7[0])
        
        
unittest.main()
