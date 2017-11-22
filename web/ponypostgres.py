from datetime import datetime, time
from pony.orm import *
# set_sql_debug(True)

db = Database()

class Nodule(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str, unique=True)
    name = Required(str)
    presence = Optional(bool)
    tags = Optional(str)
    created_at = Required(datetime)
    woken_at = Optional(datetime)
    power = Optional(float)
    lat = Optional(float)
    lon = Optional(float)
    sensors = Set('Component')
    jobs = Set('Job')
    zone = Required('Zone')


class Component(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str)
    name = Required(str)  # TODO needed?
    description = Required(str)  # What is this component doing, where is it placed?
    component_type = Required(str)  # eg DHT_11, ds18b20
    kind = Required(str)  # sensor or actuator - maybe unnecessary distinction
    pin = Required(str)  # Physical pin, i2c address etc
    nodule = Required('Nodule')
    jobs = Set('Job')  # actuators in particular may have multiple schedules


class Job(db.Entity):
    id = PrimaryKey(int, auto=True)
    uid = Required(str)
    name = Required(str)
    description = Required(str)
    period = Optional(int)
    interval = Optional(int)
    units = Required(str)
    at_time = Optional(time)
    start_day = Optional(str)
    tags = Required(str)
    component = Required('Component')
    params = Optional(Json)
    nodule = Required('Nodule')
    #   type: actuator
    # component_type = Required(str)




class Zone(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    url = Optional(str)
    description = Optional(str)
    nodules = Set(Nodule)
    children = Set('Zone', reverse='parent')
    parent = Optional('Zone', reverse='children')



class Link(db.Entity):
    id = PrimaryKey(int, auto=True)
    created_at = Required(str)
    url = Required(str)
    description = Required(str)





db.bind(provider='postgres', user='postgres', password='mysecretpassword', host='192.168.99.100', database='')
# db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
if __name__ == '__main__':

    with db_session:
        # L1 = Link(created_at='Tuesday', url='facebook.com', description='Facebook')
        # L2 = Link(created_at='Thursday', url='hackaday.com', description='HackADay')
        Z0 = Zone(name='root', url='/', description='root')
        Z1 = Zone(name='3_bayside_village', url='/3_bayside_village', description='3 Bayside Village', parent=Z0)
        Z2 = Zone(name='bedroom', url='/3_bayside_village/bedroom', description='Bedroom', parent=Z1)
        Z3 = Zone(name='living_room', url='/3_bayside_village/living_room', description='Living Room', parent=Z1)
        Z4 = Zone(name='balcony', url='/3_bayside_village/bedroom/balcony', description='Balcony', parent=Z2)
        Z5 = Zone(name='counter', url='/3_bayside_village/living_room/counter', description='Counter Top', parent=Z3)
        Z6 = Zone(name='window1', url='/3_bayside_village/living_room/window', description='Window by desk', parent=Z3)
        z_lr = Zone.get(name='living_room')
        print(z_lr.name)
        Z7 = Zone(name='SE window', url='/3_bayside_village/living_room/se_window', description='South East Window', parent=Z3)
        Z8 = Zone(name='SW window', url='/3_bayside_village/living_room/sw_window', description='South West Window', parent=Z3)

        N1 = Nodule(uid='abc123', name='balcony', created_at=datetime.now(), zone=Z4)
        N2 = Nodule(uid='def456', name='living room', created_at=datetime.now(), zone=Z3)
        N3 = Nodule(uid='ghi789', name='SE Window', created_at=datetime.now(), zone=Z7)
        N5 = Nodule(uid='jkl012', name='Sw Window', created_at=datetime.now(), zone=Z8)
        # n_bal = Nodule.get(name='balcony')
        # print(n_bal.name)
        c1 = Component(uid='111', name='balc temp/hmdy', description='balcony temperature/humidity', kind='sensor', component_type='DHT_11', pin="1", nodule=N1)
        c2 = Component(uid='222', name='tom_soil_temp', description='tomato soil temp', kind='sensor', component_type='ds18b20', pin="i2c_2", nodule=N1)
        c3 = Component(uid='333', name='aub_soil_temp', description='aubergine soil temp', kind='sensor', component_type='ds18b20', pin="i2c_3", nodule=N1)
        c4 = Component(uid='444', name='tom_soil_moist', description='tomato soil moisture', kind='sensor', component_type='moisture', pin="4", nodule=N1)
        c5 = Component(uid='555', name='aub_soil_moist', description='aubergine soil moisture', kind='sensor', component_type='moisture', pin="5", nodule=N1)
        c6 = Component(uid='666', name='balc lux', description='balcony light intensity', kind='sensor', component_type='TSL2561', pin="i2c_6", nodule=N1)

        c7 = Component(uid='777', name='window', description='greenhouse window', kind='actuator', component_type='servo', pin="7", nodule=N1)
        c8 = Component(uid='888', name='pu,p', description='irrigation pump', kind='actuator', component_type='pump', pin="8", nodule=N1)

        #
        j1 = Job(uid='zzz', name='balcony air temp', description='Balcony air temperature and humidity', interval='5', units='C/%', tags='_', component=c1, nodule=N1)
        j2 = Job(uid='yyy', name='tomato soil temp', description='Temperature of soil in tomato pot', interval='20', units='C', tags='_', component=c2, nodule=N1)
        j3 = Job(uid='xxx', name='aubergine soil temp', description='Temperature of soil in aubergine pot', interval='20', units='C', tags='_', component=c3, nodule=N1)
        j4 = Job(uid='www', name='tomato soil moisture', description='Moisture of soil in tomato pot', interval='20', units='%', tags='_', component=c4, nodule=N1)
        j5 = Job(uid='vvv', name='aubergine soil moisture', description='Moisture of soil in aubergine pot', interval='20', units='%', tags='_', component=c5, nodule=N1)
        j6 = Job(uid='uuu', name='balcony light', description='Light intensity on balcony', interval='5', units='lux', tags='_', component=c6, nodule=N1)
