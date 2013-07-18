from StringIO import StringIO

from django.db import models
import ofxclient
from ofxclient.account import Account
from ofxclient.client import Client
from ofxparse import OfxParser
from BeautifulSoup import BeautifulStoneSoup


class Institution(models.Model):
	fid = models.IntegerField()
	org = models.CharField(max_length=50)
	url = models.CharField(max_length=255)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=128)

	class Meta:
		unique_together = ("fid", "username")

	def client(self):
		"""Build a :py:class:`ofxclient.Client` for talking with the bank

		:rtype: :py:class:`ofxclient.Client`
		"""
		inst = ofxclient.Institution(str(self.fid), self.org, self.url, self.username, self.password)
		return Client(institution=inst)

	def authenticate(self):
		"""Test the authentication credentials

		Raises a ``ValueError`` if there is a problem authenticating
		with the human readable reason given by the institution.

		:param username: optional username (use self.username by default)
		:type username: string or None
		:param password: optional password (use self.password by default)
		:type password: string or None
		"""

		client = self.client()
		query = client.authenticated_query(username=u, password=p)
		res = client.post(query)
		ofx = BeautifulStoneSoup(res)

		sonrs = ofx.find('sonrs')
		code = int(sonrs.find('code').contents[0].strip())

		try:
			status = sonrs.find('message').contents[0].strip()
		except Exception:
			status = ''

		if code == 0:
			return True

		raise ValueError(status)

	def accounts(self):
		"""Ask the bank for the known :py:class:`ofxclient.Account` list.

		:rtype: list of :py:class:`ofxclient.Account` objects
		"""
		client = self.client()
		query = client.account_list_query()
		resp = client.post(query)
		resp_handle = StringIO(resp)

		parsed = OfxParser.parse(resp_handle)

		return [Account.from_ofxparse(a, institution=self)
				for a in parsed.accounts]
