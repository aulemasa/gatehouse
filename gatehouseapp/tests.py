#coding: utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from gatehouseapp.forms import VisitCreateForm
from gatehouseapp.models import VisitData


class VisitDataModelTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        VisitData.objects.create(visit_date='2017-06-23', guest="Jan Kowalski", company='Test Company',
                                 visit_host='HOST', plan_hour='13:00', arrive_hour='13:01', exit_hour='13:02',
                                 comment='Coment', key_in_user=user)

    def test_visit_data_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('visit_date').verbose_name
        self.assertEquals(field_label, 'Data wizyty')

    def test_quest_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('guest').verbose_name
        self.assertEquals(field_label, 'Imię i nazwisko gościa'.decode('utf8'))

    def test_company_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'Firma którą reprezentuje'.decode('utf8'))

    def test_visit_host_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('visit_host').verbose_name
        self.assertEquals(field_label, 'Do kogo'.decode('utf8'))

    def test_plan_hour_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('plan_hour').verbose_name
        self.assertEquals(field_label, 'Planowana godzina wizyty'.decode('utf8'))

    def test_arrive_hour_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('arrive_hour').verbose_name
        self.assertEquals(field_label, 'Godzina przybycia'.decode('utf8'))

    def test_exit_hour_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('exit_hour').verbose_name
        self.assertEquals(field_label, 'Godzina wyjścia'.decode('utf8'))

    def test_comment_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'Komentarz'.decode('utf8'))

    def test_key_in_user_label(self):
        visitdataobject = VisitData.objects.get(id=1)
        field_label = visitdataobject._meta.get_field('key_in_user').verbose_name
        self.assertEquals(field_label, 'Użytkownik'.decode('utf8'))

    def test_string_repre(self):
        visitdataobject = VisitData.objects.get(id=1)
        self.assertEqual(str(visitdataobject),
                         "%s: %s %s %s %s" % (visitdataobject.visit_date, visitdataobject.guest,
                                              visitdataobject.visit_host, visitdataobject.plan_hour,
                                              visitdataobject.key_in_user))


class VisitDataViewsTest(TestCase):
    @classmethod
    def setUp(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        VisitData.objects.create(visit_date='2017-06-23', guest="Jan Kowalski", company='Test Company',
                                 visit_host='HOST', plan_hour='13:00', arrive_hour='13:01', exit_hour='13:02',
                                 comment='Coment', key_in_user=user)
        myobject = VisitData.objects.filter(id=1)

        return myobject

    def test_homePage_url_acces_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_login_required_addVisit_view(self):
        response = self.client.get(reverse('appadmin'))
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/gatehouseadmin/')

    def test_login_required_archive_view(self):
        response = self.client.get(reverse('arch'))
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/gatehousearch/')

    def test_login_required_TodayVisitForGetehouePersonListView(self):
        response = self.client.get(reverse('todayvisit'))
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/todayvisit/')

    def test_login_required_CateringListView(self):
        response = self.client.get(reverse('cateringurl'))
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/catering')

class VisitDataFormTest(TestCase):

    def test_VisitCreateForm_valid(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        form = VisitCreateForm(data={'visit_date': '2017-06-23', 'guest': "Jan Kowalski", 'company': 'Test Company',
                                     'visit_host': 'HOST', 'plan_hour': '13:00',
                                     'comment': 'Coment', 'key_in_user': user})
        self.assertTrue(form.is_valid())

    def test_VisitCreateForm_blank_data(self):
        form = VisitCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'visit_date': [u'This field is required.'],
            'guest': [u'This field is required.'],
            'visit_host': [u'This field is required.'],
            'plan_hour': [u'This field is required.'],
        })