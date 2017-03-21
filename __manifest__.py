# -*- coding: utf-8 -*-
{
    'name': "medical",

    'summary': """
        Medical    
    """,

    'description': """
        - Medical
        - Medical Hospital
        - Medical Medicament
        - Medical Medication
        - Medical Disease
        - Medical Prescription
        - Medical Laboratory
        - Medical Imaging
        - Medical Outpatient Administration
        - Medical Inpatient Administration
    """,

    'author': "Capstone Solutions Inc.",
    'website': "http://www.capstone.ph",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account', 'account_accountant', 'point_of_sale', 'website', 'im_livechat', 'report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        # 'views/medical_sequence.xml',
        'data/ir_sequence_data.xml',
        'data/medical_ethnic_group_data.xml',
        'data/medicament/medical_medicament_drug_form_data.xml',
        'data/medicament/medical_medicament_drug_route_data.xml',
        'data/medication/medical_medication_dosage_data.xml',
        'data/appointment/medical_appointment_data.xml',
        'report/lab/medical_lab_test_report.xml',
        'report/lab/medical_lab_test_report_template.xml',
        'report/prescription/medical_prescription_order_report.xml',
        'report/prescription/medical_prescription_order_report_template.xml',
        'views/product_product_view.xml',
        'views/res_partner_view.xml',
        'views/medical_physician_view.xml',
        'views/medical_patient_view.xml',
        'views/medical_patient_family_view.xml',
        'views/medical_appointment_view.xml',
        'views/medical_specialty_view.xml',
        'views/medical_ethnic_group_view.xml',
        'security/medical_security.xml',
        'views/medical_menu.xml',
        'views/hospital/medical_hospital_bed_view.xml',
        'views/hospital/medical_hospital_room_view.xml',
        'views/hospital/medical_hospital_zone_view.xml',
        'views/hospital/medical_hospital_or_view.xml',
        'views/hospital/medical_hospital_unit_view.xml',
        'views/hospital/medical_hospital_menu.xml',
        'views/medicament/medical_medicament_product.xml',
        'views/medicament/medical_medicament_view.xml',
        'views/medicament/medical_medicament_drug_form_view.xml',
        'views/medicament/medical_medicament_drug_route_view.xml',
        'views/medicament/medical_medicament_menu.xml',
        'views/medication/medical_medication_dosage_view.xml',
        'views/medication/medical_medication_template_view.xml',
        'views/medication/medical_medication_patient_medication_view.xml',
        'views/medication/medical_medication_patient_view.xml',
        'views/medication/medical_medication_menu.xml',
        'views/disease/medical_disease_pathology_group_view.xml',
        'views/disease/medical_disease_pathology_category_view.xml',
        'views/disease/medical_disease_pathology_view.xml',
        'views/disease/medical_disease_patient_disease_view.xml',
        'views/disease/medical_disease_patient_view.xml',
        'views/disease/medical_disease_menu.xml',
        'views/prescription/medical_prescription_order_view.xml',
        'views/prescription/medical_prescription_order_line_view.xml',
        'views/prescription/medical_prescription_menu.xml',
        'views/lab/medical_lab_test_type_view.xml',
        'views/lab/medical_lab_view.xml',
        # 'views/lab/medical_lab_patient_view.xml',
        'views/lab/medical_lab_medical_patient_view.xml',
        'views/lab/medical_lab_menu.xml',
        'views/imaging/medical_imaging_test_type_view.xml',
        'views/imaging/medical_imaging_test_view.xml',
        'views/imaging/medical_imaging_request_view.xml',
        'views/imaging/medical_imaging_menu.xml',
        'views/hospitalization/medical_patient_hospitalization_view.xml',
        'views/hospitalization/medical_patient_hospitalization_transfer_view.xml',
        'views/hospitalization/medical_patient_hospitalization_icu_view.xml',
        'views/hospitalization/medical_hospitalization_menu.xml',
        'views/visit/medical_visit_view.xml',
        'views/visit/medical_visit_menu.xml',
        'views/surgery/medical_surgery_view.xml',
        'views/surgery/medical_procedure_view.xml',
        'views/surgery/medical_operating_area_view.xml',
        'views/surgery/medical_operating_sector_view.xml',
        'views/surgery/medical_surgery_menu.xml', 
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
        'demo/physician_specialty.xml',
        # 'demo/medical_medicament_demo.xml',
        # 'demo/medical_patient_demo.xml',
        'demo/disease/medical_pathology_category_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}