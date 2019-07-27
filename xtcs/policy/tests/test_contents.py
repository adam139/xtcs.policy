# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from xtcs.policy.content.project import IProject
from xtcs.policy.testing import FunctionalTesting
from xtcs.policy.testing import POLICY_INTEGRATION_TESTING as INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility
from zope.interface import alsoProvides

import transaction
import unittest as unittest


class DocumentIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])

    def test_schema(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Project')
        schema = fti.lookupSchema()
        self.assertEqual(schema.getName(), 'IProject')

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Project'
        )
        self.assertNotEquals(None, fti)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='Project'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IProject.providedBy(new_object))

    def test_adding(self):
        self.portal.invokeFactory(
            'Project',
            'doc1'
        )
        self.assertTrue(IProject.providedBy(self.portal['doc1']))

    def test_view(self):
        self.portal.invokeFactory('Project', 'document')
        document = self.portal['document']
        document.title = "My Document"
        document.description = "This is my document."
        document.text = RichTextValue(
            u"Lorem ipsum",
            'text/plain',
            'text/html'
        )
        self.request.set('URL', document.absolute_url())
        self.request.set('ACTUAL_URL', document.absolute_url())
        alsoProvides(self.request, IPloneFormLayer)
        view = document.restrictedTraverse('@@view')
        self.assertEqual(view.request.response.status, 200)
        output = view()
        self.assertTrue(output)
        self.assertTrue('My Document' in output)
        self.assertTrue('This is my document.' in output)
        self.assertTrue('Lorem ipsum' in output)

    def tearDown(self):
        if 'document' in self.portal.objectIds():
            self.portal.manage_delObjects(ids='document')
            transaction.commit()


class Allcontents(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('Project', 'folder1')

        self.portal = portal

    def test_item_types(self):
        self.assertEqual(self.portal['folder1'].id, 'folder1')


class DocumentFunctionalTest(unittest.TestCase):

    layer = FunctionalTesting

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_add_document(self):
        self.browser.open(self.portal_url)
        self.browser.getLink(url='http://nohost/plone/++add++Project').click()

        self.browser.getControl(name='form.widgets.IDublinCore.title')\
            .value = "My document"
        self.browser.getControl(name='form.widgets.IDublinCore.description')\
            .value = "This is my document."
        self.browser.getControl(name='form.widgets.IRichText.text')\
            .value = "Lorem Ipsum"
        self.browser.getControl(name='form.widgets.IShortName.id')\
            .value = "my-special-document"
        self.browser.getControl('Save').click()
        self.assertTrue(self.browser.url.endswith('my-special-document/view'))
        self.assertTrue('My document' in self.browser.contents)
        self.assertTrue('This is my document' in self.browser.contents)
        self.assertTrue('Lorem Ipsum' in self.browser.contents)
