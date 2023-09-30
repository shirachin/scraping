class Integer_field:
    def __init__(self, min=-10000, max=10000, init=None, required=False) -> None:
        self.value: int = init
        self.required: bool = required
        self.min: int = min
        self.max: int = max
        self.change: bool = False

    def validate(self) -> bool:
        if self.value == None:
            self.value = self.min
            self.change = True
        elif self.value < self.min:
            self.value = self.min
            self.change = True
        elif self.max < self.value:
            self.value = self.max
            self.change = True
        return self.change
    
    def set_param(self, value) -> bool:
        self.value = int(value)
        return self.validate()

class String_field:
    def __init__(self, init=None, required=False) -> None:
        self.value: str = init
        self.required: bool = required
        self.change: bool = False

    def validate(self) -> bool:
        if self.value.isspace():
            self.value = ''
        
    def set_param(self, value):
        self.value = value
        self.validate()

class Boolean_field:
    def __init__(self, init=False, required=False) -> None:
        self.value = init
        self.required = required

    def set_param(self, value: bool):
        self.value = value

    def toggle(self):
        self.value = not self.value

class Property_api:
    def __init__(self) -> None:
        self.id = Integer_field(required=True, min=0, max=99999999999)
        self.prefecture = String_field(required=True)
        self.address_lv1 = String_field()
        self.address_lv2 = String_field()
        self.address_lv3 = String_field()
        self.address_lv4 = String_field()
        self.address_lv5 = String_field()
        self.address_lv6 = String_field()
        self.address_lv7 = String_field()
        self.address_original = String_field(required=True)
        self.building_name = String_field(required=True)
        self.station1 = String_field()
        self.station1_time = Integer_field(min=1)
        self.station2 = String_field()
        self.station2_time = Integer_field(min=1)
        self.station3 = String_field()
        self.station3_time = Integer_field(min=1)
        self.floor_plan = String_field()
        self.floor_plan_breakdown = String_field()
        self.area = String_field()
        self.area_num = Integer_field()
        self.balcony = String_field()
        self.building_structure = String_field()
        self.n_storey_building = Integer_field(min=1)
        self.floor = Integer_field(min=1, max=self.n_storey_building)
        self.is_top_floor = Boolean_field()
        self.building_year = Integer_field()
        self.building_month = Integer_field(min=1, max=12)
        self.units = String_field()
        self.area_price = String_field()
        self.parking_car = String_field()
        self.parking_bike = String_field()
        self.parking_bicycle = String_field()
        self.main_glossy_surface = String_field()
        self.administrator = String_field()
        self.reform = String_field()
        self.renovation = String_field()
        self.hot_spring = String_field()
        self.facility = String_field()
        self.special_remarks = String_field()
        self.remarks = String_field()
        self.environment = String_field()
        self.rent = Integer_field()
        self.deposit = Integer_field()
        self.key_money = Integer_field()
        self.management_fee = String_field()
        self.maintenance_fee = String_field()
        self.sundries = String_field()
        self.mms_fee = String_field()
        self.drawing = String_field()
        self.etc_fee = String_field()
        self.guarantee = String_field()
        self.depreciation_guarantee = String_field()
        self.rental_guarantee = String_field()
        self.credit_card_payment = String_field()
        self.insurance_subscription = String_field()
        self.lump_sum = String_field()
        self.running_cost = String_field()
        self.present_condition = String_field()
        self.matricration_date = String_field()
        self.contract_period = String_field()
        self.renewal_fee = String_field()
        self.occupancy_requirement = String_field()
        self.equipment_warranty = String_field()
        self.rent_free = String_field()
        self.reward = Integer_field()
        self.pick_error = Boolean_field()
    
    def post(self):
        import requests
        res = requests.post('http://127.0.0.1:8080/api/property/', {
            'id': self.id,
            'prefecture': self.prefecture,
            'address_lv1': self.address_lv1,
            'address_lv2': self.address_lv2,
            'address_lv3': self.address_lv3,
            'address_lv4': self.address_lv4,
            'address_lv5': self.address_lv5,
            'address_lv6': self.address_lv6,
            'address_lv7': self.address_lv7,
            'address_original': self.address_original,
            'building_name': self.building_name,
            'station1': self.station1,
            'station2': self.station2,
            'station3': self.station3,
            'station1_time': self.station1_time,
            'station2_time': self.station2_time,
            'station3_time': self.station3_time,
            'floor_plan': self.floor_plan,
            'floor_plan_breakdown': self.floor_plan_breakdown,
            'area': self.area,
            'area_num': self.area_num,
            'balcony': self.balcony,
            'building_structure': self.building_structure,
            'n_storey_building': self.n_storey_building,
            'floor': self.floor,
            'is_top_floor': self.is_top_floor,
            'building_year': self.building_year,
            'building_month': self.building_month,
            'units': self.units,
            'area_price': self.area_price,
            'parking_car': self.parking_car,
            'parking_bike': self.parking_bike,
            'parking_bicycle': self.parking_bicycle,
            'main_glossy_surface': self.main_glossy_surface,
            'administrator': self.administrator,
            'reform': self.reform,
            'renovation': self.renovation,
            'hot_spring': self.hot_spring,
            'facility': self.facility,
            'special_remarks': self.special_remarks,
            'remarks': self.remarks,
            'environment': self.environment,
            'rent': self.rent,
            'deposit': self.deposit,
            'key_money': self.key_money,
            'management_fee': self.management_fee,
            'maintenance_fee': self.maintenance_fee,
            'sundries': self.sundries,
            'mms_fee': self.mms_fee,
            'drawing': self.drawing,
            'etc_fee': self.etc_fee,
            'guarantee': self.guarantee,
            'depreciation_guarantee': self.depreciation_guarantee,
            'rental_guarantee': self.rental_guarantee,
            'credit_card_payment': self.credit_card_payment,
            'insurance_subscription': self.insurance_subscription,
            'lump_sum': self.lump_sum,
            'running_cost': self.running_cost,
            'present_condition': self.present_condition,
            'matricration_date': self.matricration_date,
            'contract_period': self.contract_period,
            'renewal_fee': self.renewal_fee,
            'occupancy_requirement': self.occupancy_requirement,
            'equipment_warranty': self.equipment_warranty,
            'rent_free': self.rent_free,
            'reward': self.reward,
            'open': True,
            'correct': False
        })

        print(f'status_code : {res.status_code}')