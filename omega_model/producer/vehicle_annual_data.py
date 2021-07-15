"""


----

**CODE**

"""

print('importing %s' % __file__)

from omega_model import *

cache = dict()


class VehicleAnnualData(SQABase, OMEGABase):
    # --- database table properties ---
    __tablename__ = 'vehicle_annual_data'
    index = Column('index', Integer, primary_key=True)
    vehicle_ID = Column('vehicle_id', Integer, ForeignKey('vehicles.vehicle_id'))
    calendar_year = Column(Numeric)
    age = Column(Numeric)
    # reg_class_ID = Column(String)
    # in_use_fuel_ID = Column(String)
    registered_count = Column(Float)
    annual_vmt = Column(Float)
    vmt = Column(Float)
    # vmt_liquid_fuel = Column(Float)
    # vmt_electricity = Column(Float)
    # onroad_direct_co2e_grams_per_mile = Column(Float)
    # onroad_direct_kwh_per_mile = Column(Float)
    # onroad_gallons_per_mile = Column(Float)
    # fuel_consumption_gallons = Column(Float)
    # fuel_consumption_kWh = Column(Float)
    # voc_tailpipe_ustons = Column(Float)
    # co_tailpipe_ustons = Column(Float)
    # nox_tailpipe_ustons = Column(Float)
    # pm25_tailpipe_ustons = Column(Float)
    # so2_tailpipe_ustons = Column(Float)
    # benzene_tailpipe_ustons = Column(Float)
    # butadiene13_tailpipe_ustons = Column(Float)
    # formaldehyde_tailpipe_ustons = Column(Float)
    # acetaldehyde_tailpipe_ustons = Column(Float)
    # acrolein_tailpipe_ustons = Column(Float)
    # ch4_tailpipe_metrictons = Column(Float)
    # n2o_tailpipe_metrictons = Column(Float)
    # co2_tailpipe_metrictons = Column(Float)
    # voc_upstream_ustons = Column(Float)
    # co_upstream_ustons = Column(Float)
    # nox_upstream_ustons = Column(Float)
    # pm25_upstream_ustons = Column(Float)
    # so2_upstream_ustons = Column(Float)
    # benzene_upstream_ustons = Column(Float)
    # butadiene13_upstream_ustons = Column(Float)
    # formaldehyde_upstream_ustons = Column(Float)
    # acetaldehyde_upstream_ustons = Column(Float)
    # acrolein_upstream_ustons = Column(Float)
    # ch4_upstream_metrictons = Column(Float)
    # n2o_upstream_metrictons = Column(Float)
    # co2_upstream_metrictons = Column(Float)
    # voc_total_ustons = Column(Float)
    # co_total_ustons = Column(Float)
    # nox_total_ustons = Column(Float)
    # pm25_total_ustons = Column(Float)
    # so2_total_ustons = Column(Float)
    # benzene_total_ustons = Column(Float)
    # butadiene13_total_ustons = Column(Float)
    # formaldehyde_total_ustons = Column(Float)
    # acetaldehyde_total_ustons = Column(Float)
    # acrolein_total_ustons = Column(Float)
    # ch4_total_metrictons = Column(Float)
    # n2o_total_metrictons = Column(Float)
    # co2_total_metrictons = Column(Float)

    @staticmethod
    def update_registered_count(vehicle, calendar_year, registered_count):
        """
        Update vehicle registered count and / or create initial vehicle annual data table entry
        :param vehicle:  VehicleFinal object
        :param calendar_year: calendar year
        :param registered_count: number of vehicle that are still in service (registered)
        :return: updates vehicle annual data table
        """
        age = calendar_year - vehicle.model_year

        vad = omega_globals.session.query(VehicleAnnualData). \
            filter(VehicleAnnualData.vehicle_ID == vehicle.vehicle_ID). \
            filter(VehicleAnnualData.calendar_year == calendar_year). \
            filter(VehicleAnnualData.age == age).one_or_none()

        if vad:
            vad.registered_count = registered_count
        else:
            omega_globals.session.add(VehicleAnnualData(vehicle_ID=vehicle.vehicle_ID,
                                                        calendar_year=calendar_year,
                                                        registered_count=registered_count,
                                                        age=age))

    @staticmethod
    def update_vehicle_annual_data(vehicle, calendar_year, attribute, attribute_value):

        age = calendar_year - vehicle.model_year

        vad = omega_globals.session.query(VehicleAnnualData). \
            filter(VehicleAnnualData.vehicle_ID == vehicle.vehicle_ID). \
            filter(VehicleAnnualData.calendar_year == calendar_year). \
            filter(VehicleAnnualData.age == age).one()

        vad.__setattr__(attribute, attribute_value)

        omega_globals.session.flush()

    @staticmethod
    def get_calendar_years():
        return sql_unpack_result(omega_globals.session.query(VehicleAnnualData.calendar_year).all())

    @staticmethod
    def get_initial_registered_count():
        """

        Returns: registered count of vehicles prior to initial analysis year

        """

        cache_key = '%s_initial_registered_count' % (omega_globals.options.analysis_initial_year - 1)
        if cache_key not in cache:
            cache[cache_key] = float(
                omega_globals.session.query(func.sum(VehicleAnnualData.registered_count)).filter(
                    VehicleAnnualData.calendar_year == omega_globals.options.analysis_initial_year - 1).scalar())

        return cache[cache_key]

    @staticmethod
    def get_initial_fueling_class_registered_count(fueling_class):
        """

        Args:
            fueling_class: fueling class to filter results by

        Returns: registered count of vehicles of the given ``fueling_class`` prior to initial analysis year

        """
        cache_key = '%s_%s_initial_registered_count' % (omega_globals.options.analysis_initial_year - 1, fueling_class)
        if cache_key not in cache:
            from vehicles import VehicleFinal
            cache[cache_key] = float(
                omega_globals.session.query(func.sum(VehicleAnnualData.registered_count)).join(VehicleFinal).filter(
                    VehicleFinal.fueling_class == fueling_class).filter(
                    VehicleAnnualData.calendar_year == omega_globals.options.analysis_initial_year - 1).scalar())

        return cache[cache_key]

    @staticmethod
    def insert_vmt(vehicle_ID, calendar_year, annual_vmt):
        vmt = omega_globals.session.query(VehicleAnnualData.registered_count). \
                  filter(VehicleAnnualData.vehicle_ID == vehicle_ID). \
                  filter(VehicleAnnualData.calendar_year == calendar_year).scalar() * annual_vmt
        vad = omega_globals.session.query(VehicleAnnualData). \
            filter(VehicleAnnualData.vehicle_ID == vehicle_ID). \
            filter(VehicleAnnualData.calendar_year == calendar_year).all()
        vad[0].annual_vmt = annual_vmt
        vad[0].vmt = vmt

    @staticmethod
    def get_vehicle_annual_data(calendar_year, attributes=None):
        if attributes is None:
            return omega_globals.session.query(VehicleAnnualData).filter(VehicleAnnualData.calendar_year == calendar_year).all()
        else:
            if type(attributes) is not list:
                attributes = [attributes]
            attrs = VehicleAnnualData.get_class_attributes(attributes)

            result = omega_globals.session.query(*attrs).filter(VehicleAnnualData.calendar_year == calendar_year).all()

            return result


if __name__ == '__main__':
    try:
        if '__file__' in locals():
            print(file_io.get_filenameext(__file__))

        import importlib

        # set up global variables:
        omega_globals.options = OMEGARuntimeOptions()

        init_fail = []

        # pull in reg classes before building database tables (declaring classes) that check reg class validity
        module_name = get_template_name(omega_globals.options.policy_reg_classes_file)
        omega_globals.options.RegulatoryClasses = importlib.import_module(module_name).RegulatoryClasses
        init_fail += omega_globals.options.RegulatoryClasses.init_from_file(
            omega_globals.options.policy_reg_classes_file)

        init_omega_db(omega_globals.options.verbose)

        from producer.manufacturers import Manufacturer  # required by vehicles
        from context.onroad_fuels import OnroadFuel  # required by vehicles
        from consumer.market_classes import MarketClass  # required by vehicles
        from producer.vehicles import VehicleFinal  # for foreign key vehicle_ID

        SQABase.metadata.create_all(omega_globals.engine)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
