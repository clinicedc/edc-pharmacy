# edc-pharma
Allows pharmacists to print labels during dispensing


### Setup

    pip install git+https://github.com/botswana-harvard/edc-pharma@develop#egg=edc_pharma
    
### Usage
Protocol:

	User should add a Protocol to the system database

Site:

	Then add Sites that are linked to the aforementioned Protocol.

Patient:

	From therein, Patients from a particular Site can also be added to the 	database.

Medication:

	Furthermore, Medications depending on a particular Protocol can also be added to the database. 

Dispense:

	Whenever the user dispenses a prescription, he/she should add the Dispense to the system, indicating the Patient, Medication and other information relevant during dispensing eg drug dosage and frequency per day..

