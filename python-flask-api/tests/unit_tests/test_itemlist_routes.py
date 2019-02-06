from flask import json
from peewee import *
import pytest

from db import seed
from models import ItemList

from main import app

client = app.test_client()

class TestItemlistRoutes:
    @classmethod
    def setup_method(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        seed()

    def test_get_all_itemlists(self):
        response = client.get('/lists')
        itemlists = json.loads(response.data)
        assert len(itemlists) == 2

    def test_create_itemlist_success(self):
        body = { 'name': 'Test' }
        response = client.post('/lists', json=body)
        itemlist = json.loads(response.data)
        assert itemlist['name'] == 'Test'

    def test_create_itemlist_failure(self):
        body = { 'name': None }
        response = client.post('/lists', json=body)

        with pytest.raises(Exception):
            itemlist = json.loads(response.data)

    # Not-Implemented

    def test_get_itemlist(self):
        itemlist_id = ItemList.select().get().id

        response = client.get('/lists/{}'.format(itemlist_id))
        itemlist = json.loads(response.data)
        assert itemlist['id']

    def test_update_itemlist_success(self):
        itemlist_id = ItemList.select().get().id

        body = { 'name': 'Test' }
        response = client.put('/lists/{}'.format(itemlist_id), json=body)
        itemlist = json.loads(response.data)
        assert itemlist['name'] == 'Test'

    def test_update_itemlist_failure(self):
        itemlist_id = ItemList.select().get().id

        body = { 'name': None }
        response = client.put('/lists/{}'.format(itemlist_id), json=body)

        with pytest.raises(Exception):
            itemlist = json.loads(response.data)

    def test_delete_itemlist(self):
        itemlist_id = ItemList.select().get().id

        client.delete('/lists/{}'.format(itemlist_id))
        with pytest.raises(DoesNotExist):
            assert ItemList.get_by_id(itemlist_id)