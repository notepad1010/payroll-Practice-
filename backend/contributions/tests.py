from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal
from security.models import UserAccount
from payroll.models import DeductionType
from contributions.models import (
    SSSContribution, 
    PagIBIGContribution, 
    PhilhealthContribution, 
    WithHoldingTaxBracket
)


class BaseContributionTestCase(APITestCase):
    """Base test case with authentication setup"""

    def setUp(self):
        # Create test user
        self.user = UserAccount.objects.create_superuser(
            username='testuser',
            password='Test@1234',
            email='test@payroll.com',
            company_email='test@payroll.com'
        )

        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'Test@1234'
        })
        self.token = response.data['access']

        # Set auth header
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        # Create test deduction types
        self.sss_deduction = DeductionType.objects.create(
            deduction_name='SSS Contribution',
            is_taxable=False,
            description='Social Security System'
        )

        self.pagibig_deduction = DeductionType.objects.create(
            deduction_name='PagIBIG Contribution',
            is_taxable=False,
            description='Pag-IBIG Fund'
        )

        self.philhealth_deduction = DeductionType.objects.create(
            deduction_name='PhilHealth Contribution',
            is_taxable=False,
            description='Philippine Health Insurance'
        )

        self.withholding_tax_deduction = DeductionType.objects.create(
            deduction_name='Withholding Tax',
            is_taxable=True,
            description='Income Tax Withholding'
        )


# ─── SSS Contribution Tests ───────────────────────────────────────

class SSSContributionTests(BaseContributionTestCase):

    def test_create_sss_contribution(self):
        """Test creating a new SSS contribution"""
        sss = SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=date.today()
        )
        self.assertEqual(str(sss), f"SSS Contribution: {sss.max_salary} - {sss.min_salary}")
        self.assertEqual(sss.base_tax, Decimal('50.00'))

    def test_sss_contribution_fields(self):
        """Test SSS contribution model fields"""
        sss = SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=date.today()
        )
        self.assertIsNotNone(sss.create_at)
        self.assertIsNotNone(sss.update_at)

    def test_sss_contribution_with_end_date(self):
        """Test SSS contribution with end date"""
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        sss = SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=start_date,
            effective_end_date=end_date
        )
        self.assertEqual(sss.effective_end_date, end_date)

    def test_multiple_sss_salary_brackets(self):
        """Test creating multiple SSS salary brackets"""
        brackets = [
            {
                'deduction_type': self.sss_deduction,
                'min_salary': Decimal('1000.00'),
                'max_salary': Decimal('2000.00'),
                'base_tax': Decimal('25.00'),
                'tax_rate': Decimal('3.00'),
                'excess_over': Decimal('1000.00'),
                'effective_start_date': date.today()
            },
            {
                'deduction_type': self.sss_deduction,
                'min_salary': Decimal('2000.01'),
                'max_salary': Decimal('5000.00'),
                'base_tax': Decimal('55.00'),
                'tax_rate': Decimal('3.50'),
                'excess_over': Decimal('2000.00'),
                'effective_start_date': date.today()
            }
        ]
        for bracket in brackets:
            SSSContribution.objects.create(**bracket)
        
        sss_contributions = SSSContribution.objects.all()
        self.assertEqual(sss_contributions.count(), 2)


# ─── PagIBIG Contribution Tests ───────────────────────────────────────

class PagIBIGContributionTests(BaseContributionTestCase):

    def test_create_pagibig_contribution(self):
        """Test creating a new PagIBIG contribution"""
        data = {
            'deduction_type': self.pagibig_deduction,
            'min_salary': Decimal('1000.00'),
            'max_salary': Decimal('5000.00'),
            'employee_share_rate': Decimal('1.00'),
            'employer_share_rate': Decimal('2.00'),
            'max_employee_share': Decimal('100.00'),
            'max_employer_share': Decimal('200.00'),
            'effective_start_date': date.today()
        }
        pagibig = PagIBIGContribution.objects.create(**data)
        self.assertIn('PagIBIG', str(pagibig))
        self.assertEqual(pagibig.employee_share_rate, Decimal('1.00'))

    def test_pagibig_employee_employer_rates(self):
        """Test PagIBIG employee and employer rates"""
        pagibig = PagIBIGContribution.objects.create(
            deduction_type=self.pagibig_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            employee_share_rate=Decimal('1.50'),
            employer_share_rate=Decimal('2.00'),
            max_employee_share=Decimal('150.00'),
            max_employer_share=Decimal('200.00'),
            effective_start_date=date.today()
        )
        self.assertEqual(pagibig.employee_share_rate, Decimal('1.50'))
        self.assertEqual(pagibig.employer_share_rate, Decimal('2.00'))
        self.assertGreater(pagibig.employer_share_rate, pagibig.employee_share_rate)

    def test_pagibig_max_share_limits(self):
        """Test PagIBIG maximum share limits"""
        pagibig = PagIBIGContribution.objects.create(
            deduction_type=self.pagibig_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('10000.00'),
            employee_share_rate=Decimal('1.50'),
            employer_share_rate=Decimal('2.00'),
            max_employee_share=Decimal('150.00'),
            max_employer_share=Decimal('200.00'),
            effective_start_date=date.today()
        )
        self.assertEqual(pagibig.max_employee_share, Decimal('150.00'))
        self.assertEqual(pagibig.max_employer_share, Decimal('200.00'))

    def test_multiple_pagibig_brackets(self):
        """Test creating multiple PagIBIG salary brackets"""
        brackets = [
            {
                'deduction_type': self.pagibig_deduction,
                'min_salary': Decimal('1000.00'),
                'max_salary': Decimal('3000.00'),
                'employee_share_rate': Decimal('1.00'),
                'employer_share_rate': Decimal('2.00'),
                'max_employee_share': Decimal('30.00'),
                'max_employer_share': Decimal('60.00'),
                'effective_start_date': date.today()
            },
            {
                'deduction_type': self.pagibig_deduction,
                'min_salary': Decimal('3000.01'),
                'max_salary': Decimal('10000.00'),
                'employee_share_rate': Decimal('1.50'),
                'employer_share_rate': Decimal('2.00'),
                'max_employee_share': Decimal('150.00'),
                'max_employer_share': Decimal('200.00'),
                'effective_start_date': date.today()
            }
        ]
        for bracket in brackets:
            PagIBIGContribution.objects.create(**bracket)
        
        pagibig_contributions = PagIBIGContribution.objects.all()
        self.assertEqual(pagibig_contributions.count(), 2)


# ─── PhilHealth Contribution Tests ───────────────────────────────────────

class PhilhealthContributionTests(BaseContributionTestCase):

    def test_create_philhealth_contribution(self):
        """Test creating a new PhilHealth contribution"""
        data = {
            'deduction_type': self.philhealth_deduction,
            'premium_rate': Decimal('5.00'),
            'salary_floor': Decimal('1000.00'),
            'salary_ceiling': Decimal('50000.00'),
            'employee_share_ratio': Decimal('0.5000'),
            'employer_share_ratio': Decimal('0.5000'),
            'effective_start_date': date.today()
        }
        philhealth = PhilhealthContribution.objects.create(**data)
        self.assertIn('philhealth_rate', str(philhealth))
        self.assertEqual(philhealth.premium_rate, Decimal('5.00'))

    def test_philhealth_share_ratios(self):
        """Test PhilHealth employee and employer share ratios"""
        philhealth = PhilhealthContribution.objects.create(
            deduction_type=self.philhealth_deduction,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('1000.00'),
            salary_ceiling=Decimal('50000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=date.today()
        )
        # Verify ratios sum to 1.0
        total_ratio = philhealth.employee_share_ratio + philhealth.employer_share_ratio
        self.assertEqual(total_ratio, Decimal('1.0000'))

    def test_philhealth_salary_bounds(self):
        """Test PhilHealth salary floor and ceiling"""
        philhealth = PhilhealthContribution.objects.create(
            deduction_type=self.philhealth_deduction,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('1000.00'),
            salary_ceiling=Decimal('50000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=date.today()
        )
        self.assertEqual(philhealth.salary_floor, Decimal('1000.00'))
        self.assertEqual(philhealth.salary_ceiling, Decimal('50000.00'))
        self.assertLess(philhealth.salary_floor, philhealth.salary_ceiling)

    def test_philhealth_with_end_date(self):
        """Test PhilHealth contribution with end date"""
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        philhealth = PhilhealthContribution.objects.create(
            deduction_type=self.philhealth_deduction,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('1000.00'),
            salary_ceiling=Decimal('50000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=start_date,
            effective_end_date=end_date
        )
        self.assertEqual(philhealth.effective_end_date, end_date)


# ─── Withholding Tax Tests ───────────────────────────────────────

class WithHoldingTaxBracketTests(BaseContributionTestCase):

    def test_create_withholding_tax_bracket(self):
        """Test creating a new withholding tax bracket"""
        data = {
            'deduction_type': self.withholding_tax_deduction,
            'min_salary': Decimal('0.00'),
            'max_salary': Decimal('10000.00'),
            'base_tax': Decimal('0.00'),
            'tax_rate': Decimal('5.00'),
            'excess_over': Decimal('0.00'),
            'effective_start_date': date.today()
        }
        tax_bracket = WithHoldingTaxBracket.objects.create(**data)
        self.assertIn('TAX BRACKET', str(tax_bracket))

    def test_multiple_tax_brackets(self):
        """Test creating multiple tax brackets"""
        brackets = [
            {
                'deduction_type': self.withholding_tax_deduction,
                'min_salary': Decimal('0.00'),
                'max_salary': Decimal('10000.00'),
                'base_tax': Decimal('0.00'),
                'tax_rate': Decimal('5.00'),
                'excess_over': Decimal('0.00'),
                'effective_start_date': date.today()
            },
            {
                'deduction_type': self.withholding_tax_deduction,
                'min_salary': Decimal('10000.01'),
                'max_salary': Decimal('30000.00'),
                'base_tax': Decimal('500.00'),
                'tax_rate': Decimal('10.00'),
                'excess_over': Decimal('10000.00'),
                'effective_start_date': date.today()
            },
            {
                'deduction_type': self.withholding_tax_deduction,
                'min_salary': Decimal('30000.01'),
                'max_salary': Decimal('9999999.99'),
                'base_tax': Decimal('2500.00'),
                'tax_rate': Decimal('15.00'),
                'excess_over': Decimal('30000.00'),
                'effective_start_date': date.today()
            }
        ]
        for bracket in brackets:
            WithHoldingTaxBracket.objects.create(**bracket)
        
        tax_brackets = WithHoldingTaxBracket.objects.all()
        self.assertEqual(tax_brackets.count(), 3)

    def test_tax_bracket_progression(self):
        """Test tax brackets follow progressive rate structure"""
        bracket1 = WithHoldingTaxBracket.objects.create(
            deduction_type=self.withholding_tax_deduction,
            min_salary=Decimal('0.00'),
            max_salary=Decimal('10000.00'),
            base_tax=Decimal('0.00'),
            tax_rate=Decimal('5.00'),
            excess_over=Decimal('0.00'),
            effective_start_date=date.today()
        )

        bracket2 = WithHoldingTaxBracket.objects.create(
            deduction_type=self.withholding_tax_deduction,
            min_salary=Decimal('10000.01'),
            max_salary=Decimal('30000.00'),
            base_tax=Decimal('500.00'),
            tax_rate=Decimal('10.00'),
            excess_over=Decimal('10000.00'),
            effective_start_date=date.today()
        )

        self.assertLess(bracket1.tax_rate, bracket2.tax_rate)
        self.assertLess(bracket1.max_salary, bracket2.min_salary)

    def test_withholding_tax_with_end_date(self):
        """Test withholding tax bracket with end date"""
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        tax_bracket = WithHoldingTaxBracket.objects.create(
            deduction_type=self.withholding_tax_deduction,
            min_salary=Decimal('0.00'),
            max_salary=Decimal('10000.00'),
            base_tax=Decimal('0.00'),
            tax_rate=Decimal('5.00'),
            excess_over=Decimal('0.00'),
            effective_start_date=start_date,
            effective_end_date=end_date
        )
        self.assertEqual(tax_bracket.effective_end_date, end_date)


# ─── Cross-Model Tests ───────────────────────────────────────

class ContributionIntegrationTests(BaseContributionTestCase):

    def test_contribution_foreign_key_relationship(self):
        """Test contribution models maintain relationship with deduction types"""
        sss = SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=date.today()
        )
        self.assertEqual(sss.deduction_type, self.sss_deduction)

    def test_all_contribution_types_present(self):
        """Test all contribution types can be created"""
        # Create one of each
        SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=date.today()
        )

        PagIBIGContribution.objects.create(
            deduction_type=self.pagibig_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            employee_share_rate=Decimal('1.00'),
            employer_share_rate=Decimal('2.00'),
            max_employee_share=Decimal('100.00'),
            max_employer_share=Decimal('200.00'),
            effective_start_date=date.today()
        )

        PhilhealthContribution.objects.create(
            deduction_type=self.philhealth_deduction,
            premium_rate=Decimal('5.00'),
            salary_floor=Decimal('1000.00'),
            salary_ceiling=Decimal('50000.00'),
            employee_share_ratio=Decimal('0.5000'),
            employer_share_ratio=Decimal('0.5000'),
            effective_start_date=date.today()
        )

        WithHoldingTaxBracket.objects.create(
            deduction_type=self.withholding_tax_deduction,
            min_salary=Decimal('0.00'),
            max_salary=Decimal('10000.00'),
            base_tax=Decimal('0.00'),
            tax_rate=Decimal('5.00'),
            excess_over=Decimal('0.00'),
            effective_start_date=date.today()
        )

        self.assertEqual(SSSContribution.objects.count(), 1)
        self.assertEqual(PagIBIGContribution.objects.count(), 1)
        self.assertEqual(PhilhealthContribution.objects.count(), 1)
        self.assertEqual(WithHoldingTaxBracket.objects.count(), 1)

    def test_contribution_effective_dates(self):
        """Test contribution effective date tracking"""
        start_date = date.today()
        sss = SSSContribution.objects.create(
            deduction_type=self.sss_deduction,
            min_salary=Decimal('1000.00'),
            max_salary=Decimal('5000.00'),
            base_tax=Decimal('50.00'),
            tax_rate=Decimal('3.50'),
            excess_over=Decimal('1000.00'),
            effective_start_date=start_date
        )
        self.assertEqual(sss.effective_start_date, start_date)
        self.assertIsNone(sss.effective_end_date)
