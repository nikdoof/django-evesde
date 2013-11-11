import sqlite3
from django.core.management.base import BaseCommand
from django.db import transaction, connection
from evesde.models import *


class Command(BaseCommand):
    help = 'Extracts data from the sqlite version of the SDE to the database.'

    def handle(self, *args, **options):
        dbfile = args[0]
        try:
            conn = sqlite3.connect(dbfile)
        except:
            print("Unable to open the SDE file at %s" % dbfile)

        print "Emptying existing tables..."
        with transaction.atomic():
            cursor = connection.cursor()
            for mdl in [Region, Constellation, System]:
                cursor.execute('DELETE FROM "{0}"'.format(mdl._meta.db_table))

        objs = []

        # eveUnits
        print "Importing eveUnits..."
        conn.execute("""SELECT unitID, unitName, displayName FROM eveUnits""")
        for row in conn.fetchall():
            objs.append(UnitType(pk=row[0], name=row[1], display_name=row[2] or ''))

        # dgmAttributeTypes
        print "Importing dgmAttributeTypes..."
        conn.execute("""SELECT attributeID, attributeName, displayName, unitID FROM dgmAttributeTypes""")
        for row in conn.fetchall():
            objs.append(AttributeType(pk=row[0], name=row[1], display_name=row[2] or '', unit_id=row[3]))

        # invCategories
        print "Importing invCategories..."
        conn.execute("""SELECT categoryID, categoryName FROM invCategories""")
        for row in conn.fetchall():
            objs.append(TypeCategory(pk=row[0], name=row[1]))

        # invGroups
        print "Importing invGroups..."
        conn.execute("""SELECT groupID, groupName, categoryID FROM invGroups""")
        for row in conn.fetchall():
            objs.append(TypeGroup(pk=row[0], name=row[1], category_id=row[2]))

        # invTypes
        print "Importing invTypes..."
        conn.execute("""SELECT typeID, typeName, capacity, groupID FROM invTypes""")
        for row in conn.fetchall():
            objs.append(Type(pk=row[0], name="".join(i for i in row[1] if ord(i)<128), capacity=row[2], group_id=row[3]))

        # dgmTypeAttributes
        print "Importing dgmTypeAttributes..."
        conn.execute("""SELECT typeID, attributeID, valueInt, valueFloat FROM dgmTypeAttributes""")
        for row in conn.fetchall():
             objs.append(TypeAttribute(type_id=row[0], attribute_id=row[1], valueint=row[2], valuefloat=row[3]))

        # mapDenormalized
        print "Importing mapDenormalize..."
        conn.execute("""SELECT itemID, typeID, groupID, solarSystemID, constellationID, regionID, orbitID, x, y, z, itemName FROM mapDenormalize WHERE typeID in (3, 4, 5, 14) OR groupID = 7""")
        for row in conn.fetchall():
            id, type, group, solarid, constellationid, regionid, orbitid, x, y, z, name = row

            if int(type) == 3:
                objs.append(Region(pk=id, name=name, x=0, y=0, z=0))
            elif int(type) == 4:
                objs.append(Constellation(pk=id, name=name, region_id=regionid,  x=0, y=0, z=0))
            elif int(type) == 5:
                objs.append(System(pk=id, name=name, constellation_id=constellationid, x=0, y=0, z=0))
            elif int(group) == 7:
                objs.append(Planet(pk=id, name=name, system_id=solarid, x=x, y=y, z=z))
            elif int(type) == 14:
                objs.append(Moon(pk=id, name=name, planet_id=orbitid, x=x, y=y, z=z))
        print "Done"

        # mapSolarSystemJumps
        print "Importing Jumps..."
        with transaction.atomic():
            for row in conn.execute("""SELECT fromSolarSystemID, toSolarSystemID FROM mapSolarSystemJumps"""):
                frm, to = row
                objs.append(SystemJump(to_system_id=to, from_system_id=frm))

        print 'Processing %d objects... ' % len(objs)
        with transaction.atomic():
            for i, x in enumerate(objs, start=1):
                if i % 1000 == 0: print "%d/%d (%d%%)" % (i, len(objs), round(i/len(objs) * 100))
                x.save()
        print 'Commited'


