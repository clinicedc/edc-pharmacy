import factory
from django.test import TestCase
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from factories import DispensingFactory
from ph_dispenser.models import DispensingIdentifierModel, IdentifierSequence
from edc.core.identifier.models import Sequence


class ModelTests(TestCase):

    def test_model(self):
        n = 0
        for x in range(1, 100):
            registered_subject = RegisteredSubjectFactory(sid=factory.Sequence(lambda n: '{0}'.format(n)))
            print '{1}/100 registered_subject {0}'.format(registered_subject.subject_identifier, x)
            for y in range(1, 100):
                n += 1
                dispensing = DispensingFactory(subject_identifier=registered_subject.subject_identifier, sid=registered_subject.sid, initials=registered_subject.initials)
                #print '    Dispensing {0}'.format(dispensing)
                self.assertIsNotNone(dispensing.identifier)
                #print '    assert identifier tracked'
                self.assertEqual(DispensingIdentifierModel.objects.filter(identifier=dispensing.identifier).count(), 1)
                self.assertEqual(DispensingIdentifierModel.objects.all().count(), n)
                #print '    assert not using bhp_identifier sequence table'
                self.assertEqual(Sequence.objects.all().count(), 0)
                #print '    assert using ph_dispenser.IdentifierSequence'
                self.assertEqual(IdentifierSequence.objects.all().count(), n)
