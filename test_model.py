import unittest
import schema
import seed
import os
import model

class TestModelFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        # runs after any tests
        pass

    def testLookupPrice(self):
        price = model.lookup_price('tsla')
        self.assertGreater(price, 0.01, "TSLA's price is greater than once cent.")


class TestAccountCreateAndLoad(unittest.TestCase):

    def setUp(self):
        schema.setup("test.db")
        schema.run()
        seed.run("test.db")
        model.opencursor.setDB("test.db")
        self.account = model.Account(username="carter", password="password!")

    def tearDown(self):
        os.remove("test.db")

    def testUserAdmin(self):
        a = model.Account(username="carter", password="password!")
        self.assertTrue(a.user_admin(), "user is admin")

        a2 = model.Account(username="sero", password="password!")
        self.assertFalse(a2.user_admin(), "user is admin")        

if __name__ == '__main__':
    unittest.main()