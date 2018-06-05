#-*- coding: UTF-8 -*-
import datetime
import unittest
from zope.interface import alsoProvides
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.interfaces import IPloneFormLayer
from xtcs.policy.testing import POLICY_INTEGRATION_TESTING as INTEGRATION_TESTING
from xtcs.policy.setuphandlers import STRUCTURE,_create_content
from xtcs.policy.migration import _create_article
#sqlarchemy
from sqlalchemy import text
from sqlalchemy import func
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark


class TestParametersDatabase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
#         self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        for item in STRUCTURE:
            _create_content(item, self.portal)

#     def test_article_get(self):
#         from xtcs.policy.mapping_db import  Article
#         from xtcs.policy.interfaces import IArticleLocator
#         from zope.component import getUtility
#         from xtcs.policy import Session as session
# 
#         locator = getUtility(IArticleLocator)
#         #getModel
#         id = 200
#         title = u"test article"
#         pubtime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         content = u"<p>test article</p>"
#         sortparentid = 2018
#         sortchildid = 1        
#         article = locator.getByCode(id)
#         #addModel
# 
#         if article == None:
#             locator.add(id=id,title=title,pubtime=pubtime,content= content)
#         else:
#             # remove old  delete
#             locator.DeleteByCode(id)
#             locator.add(id=id,title=title,pubtime=pubtime,content= content)
# 
#         article = locator.getByCode(id)
#         self.assertEqual(article.id,id)
#         # query pagenation 分页查询
#         articles = locator.query(start=0,size=1,id=id)
# 
#         self.assertEqual(len(articles),1)

    def test_article_query(self):
        from xtcs.policy.mapping_db import  Article
        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IArticleLocator)        
        articles = locator.query(start=0,size=10,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:
            return
        import pdb
        pdb.set_trace()
        self.assertEqual(len(articles),10)

    def test_import_article(self):
        from xtcs.policy.mapping_db import  Article
        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility

        locator = getUtility(IArticleLocator)
        articles = locator.query(start=0,size=3,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:return

        for article in articles:                                  
            docid = str(article.id)      
            container=self.portal['cishanzixun']['cishandongtai']
            _create_article(article,container)
            document = self.portal['cishanzixun']['cishandongtai'][docid]

            self.request.set('URL', document.absolute_url())
            self.request.set('ACTUAL_URL', document.absolute_url())
            alsoProvides(self.request, IPloneFormLayer)
            view = document.restrictedTraverse('@@view')
            self.assertEqual(view.request.response.status, 200)
            output = view()
            self.assertTrue(output)
#         self.assertTrue('My Document' in output)
#             self.assertTrue('This is my document.' in output)
#         self.assertTrue('Lorem ipsum' in output)

    def test_article_pubtime(self):

        from xtcs.policy.interfaces import IArticleLocator
        from zope.component import getUtility
        locator = getUtility(IArticleLocator)
        articles = locator.query(start=0,size=1,multi=1,sortparentid=1003,sortchildid=3)
        if articles == None:return
        container = self.portal['cishanzixun']['cishandongtai']
        for article in articles:                                  
            _create_article(article,container)
            doc = container[str(article.id)]
            pubtime = datetime.datetime.utcfromtimestamp(article.pubtime)
            self.assertTrue(doc.created().strftime("Y-%m-%d") == pubtime.strftime("Y-%m-%d"))
            
    def tearDown(self):
        if 'document' in self.portal.objectIds():
            self.portal.manage_delObjects(ids='document')
            transaction.commit()

    def test_project_query(self):
        from xtcs.policy.mapping_db import  Project
        from xtcs.policy.interfaces import IProjectLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IProjectLocator)        
        articles = locator.query(start=0,size=100,multi=1,sortparentid=1003,id=3)
        if articles == None:
            return
        self.assertEqual(len(articles),3)

    def test_Donor_query(self):
        from xtcs.policy.mapping_db import  Donor
        from xtcs.policy.interfaces import IDonorLocator
        from zope.component import getUtility


        locator = getUtility(IDonorLocator)        
        articles = locator.query(start=0,size=180,multi=1,did=7,id=18)

        if articles == None:
            return
        self.assertEqual(len(articles),100)

    def test_donate_query(self):

        from xtcs.policy.interfaces import IDonateLocator
        from zope.component import getUtility


        locator = getUtility(IDonateLocator)
        
        articles = locator.query(start=0,size=100,multi=1,did=18,sortchildid=3)
        if articles == None:
            return
        self.assertEqual(len(articles),4)

    def test_volunteerteam_query(self):
        from xtcs.policy.mapping_db import  Volunteerteam
        from xtcs.policy.interfaces import IVolunteerteamLocator
        from zope.component import getUtility
        from xtcs.policy import Session as session

        locator = getUtility(IVolunteerteamLocator)
        
        articles = locator.query(start=0,size=100,multi=1,did=18,id=2)
        if articles == None:
            return
        self.assertEqual(len(articles),2)


#     def test_screening_locator_cinema_lookup(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         Session.flush()
#
#         portal = self.layer['portal']
#         setRoles(portal, TEST_USER_ID, ('Manager',))
#
#         portal.invokeFactory('optilux.CinemaFolder', 'cinemas', title=u"Cinemas")
#
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema1',
#                 title=u"Cinema 1", description=u"First cinema",
#                 cinemaCode=u"ABC1",
#             )
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema2',
#                 title=u"Cinema 2", description=u"Second cinema",
#                 cinemaCode=u"ABC2",
#             )
#
#         locator = getUtility(IScreeningLocator)
#
#         cinemas = locator.cinemasForFilm(u"DEF1",
#                 datetime.datetime(2011, 1, 1, 0, 0, 0),
#                 datetime.datetime(2011, 1, 1, 23, 59, 59),
#             )
#
#         self.assertEqual(cinemas, [{'address': 'First cinema',
#                                     'cinemaCode': 'ABC1',
#                                     'name': 'Cinema 1',
#                                     'url': 'http://nohost/plone/cinemas/cinema1'}])
#
#     def test_screening_locator_screening_lookup(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#
#         screeningId = None
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         Session.flush()
#
#         screeningId = model.screeningId
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         Session.flush()
#
#         locator = getUtility(IScreeningLocator)
#
#         model = locator.screeningById(screeningId)
#
#         self.assertEqual(model.cinemaCode, u"ABC1")
#         self.assertEqual(model.filmCode, u"DEF1")
#
#     def test_screening_locator_screening_listing(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.interfaces import IScreeningLocator
#         from zope.component import getUtility
#         from z3c.saconfig import Session
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF2"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#         Session.add(model)
#
#         Session.flush()
#
#         portal = self.layer['portal']
#         setRoles(portal, TEST_USER_ID, ('Manager',))
#
#         portal.invokeFactory('optilux.CinemaFolder', 'cinemas', title=u"Cinemas")
#
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema1',
#                 title=u"Cinema 1", description=u"First cinema",
#                 cinemaCode=u"ABC1",
#             )
#         portal['cinemas'].invokeFactory('optilux.Cinema', 'cinema2',
#                 title=u"Cinema 2", description=u"Second cinema",
#                 cinemaCode=u"ABC2",
#             )
#
#         portal.invokeFactory('optilux.FilmFolder', 'films', title=u"Films")
#
#         portal['films'].invokeFactory('optilux.Film', 'film1',
#                 title=u"Film 1", description=u"First film", filmCode=u"DEF1",
#             )
#         portal['films'].invokeFactory('optilux.Film', 'film2',
#                 title=u"Film 2", description=u"Second film", filmCode=u"DEF2",
#             )
#
#         locator = getUtility(IScreeningLocator)
#         screenings = locator.screenings(u"DEF1", u"ABC1",
#                 datetime.datetime(2011, 1, 1, 0, 0, 0),
#                 datetime.datetime(2011, 1, 1, 23, 59, 59),
#             )
#
#         self.assertEqual(len(screenings), 1)
#         self.assertEqual(screenings[0].filmCode, u"DEF1")
#         self.assertEqual(screenings[0].cinemaCode, u"ABC1")
#         self.assertEqual(screenings[0].remainingTickets, 10)
#
#     def test_ticket_reserver(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.reservation import Reservation
#         from xtcs.policy.interfaces import ITicketReserver
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 10
#
#         Session.add(model)
#         Session.flush()
#
#         reservation = Reservation()
#         reservation.numTickets = 2
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#
#         reserver = getUtility(ITicketReserver)
#         reserver(reservation)
#
#         Session.flush()
#
#         self.assertTrue(reservation.reservationId is not None)
#         self.assertEqual(model.remainingTickets, 8)
#
#     def test_ticket_reserver_no_remaining_tickets(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.reservation import Reservation
#
#         from xtcs.policy.interfaces import ITicketReserver
#         from xtcs.policy.interfaces import ReservationError
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#
#         model = Screening()
#         model.cinemaCode = u"ABC1"
#         model.filmCode = u"DEF1"
#         model.showTime = datetime.datetime(2011, 1, 1, 12, 0, 0)
#         model.remainingTickets = 0
#
#         Session.add(model)
#         Session.flush()
#
#         reservation = Reservation()
#         reservation.numTickets = 2
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#
#         reserver = getUtility(ITicketReserver)
#
#         self.assertRaises(ReservationError, reserver, reservation)
#
#     def test_ticket_reserver_insufficient_tickets(self):
#         from xtcs.policy.model import Screening
#         from xtcs.policy.reservation import Reservation
#
#         from xtcs.policy.interfaces import ITicketReserver
#         from xtcs.policy.interfaces import ReservationError
#         from z3c.saconfig import Session
#         from zope.component import getUtility
#
#         model = Model()
#         model.xhdm = u"ABC1"
#         model.xhmc = u"DEF1"
#
#
#         Session.add(model)
#         Session.flush()
#
#         reservation = Reservation()
#         reservation.numTickets = 11
#         reservation.customerName = u"John Smith"
#         reservation.model = model
#
#         reserver = getUtility(ITicketReserver)
#
#         self.assertRaises(ReservationError, reserver, reservation)
