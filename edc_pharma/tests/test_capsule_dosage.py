from django.test import TestCase, tag

from ..medications import CapsuleDosage


@tag('test_capsule')
class TestCapsuleDrugDosage(TestCase):

    def test_round(self):
        capsule_dosage = CapsuleDosage()
        self.assertEqual(capsule_dosage.round(value=1.2), 2)

    def test_round_1(self):
        capsule_dosage = CapsuleDosage()
        self.assertEqual(capsule_dosage.round(value=1.7), 2)

    def test_required_quantity(self):
        """Assert number of capsules."""
        capsule_dosage = CapsuleDosage(
            body_weight=40.0, strength=500,
            millgrams_per_vial=100, duration=7, use_body_weight=True)
        self.assertTrue(capsule_dosage.required_quantity, 56)

    def test_required_quantity_1(self):
        """Assert number of vialz. (Single Dose)."""
        capsule_dosage = CapsuleDosage(
            body_weight=40.0, strength=50,
            millgrams_per_vial=10, duration=1, use_body_weight=True)
        self.assertTrue(capsule_dosage.required_quantity, 10)

    def test_required_quantity_2(self):
        """Assert number of vialz. (Single Dose)."""
        capsule_dosage = CapsuleDosage(
            strength=200, millgrams_per_vial=1200, duration=14,
            use_body_weight=False)
        self.assertTrue(capsule_dosage.required_quantity, 42)
