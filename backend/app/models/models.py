from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Ship(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    ship_type = fields.CharField(max_length=255)
    reporting_period = fields.DateField()
    doc_issue_date = fields.DateField()
    doc_expiry_date = fields.DateField()
    annual_average_co2_emissions = fields.FloatField()
    total_co2_emissions = fields.FloatField()
    technical_efficiency = fields.FloatField()

    class Meta:
        table = "ships"

    def __str__(self) -> str:
        return self.name


Ship_Pydantic = pydantic_model_creator(Ship, name="Ship")
ShipIn_Pydantic = pydantic_model_creator(Ship, name="ShipIn", exclude_readonly=True)
