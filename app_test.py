from flask import Flask, jsonify
from flask_testing import TestCase
import unittest
import index


class MyTest(TestCase):


    def create_app(self):

        app = index.app;
        app.config['TESTING'] = True
        return app

    def test_assert_maintemplate_used(self):
        response = self.client.get("/")
        self.assert_template_used("index.html")

    def test_assert_boardtemplate_used(self):
        response = self.client.get("/mboard/1")
        self.assert_template_used("board.html")
        

    def test_server_is_up_and_running(self):
        response = self.client.get("/")
        self.assertEqual(response.status, "200 OK")


    def test_db_board_exists(self):
        rv = index.get_board_items()
        assert (len(rv)>0), 'No entries here so far' 


    def test_board_gen(self):
        brd = index.board_gen()
        err=0        
        for ind in range(len(brd)):
            if brd.count(ind+1) !=1:
                err+=1
        assert err==0, 'Generated board is incorrect' 



if __name__ == '__main__':
    unittest.main()
