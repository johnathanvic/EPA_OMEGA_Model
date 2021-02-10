"""
stock.py
========

"""

from usepa_omega2 import *

vmt_dict = dict()
def get_annual_vmt(calendar_year, market_class_ID, model_year, query=False):
    # get annual vmt
    age = (calendar_year - model_year)

    annual_vmt_id = '%s_%s' % (market_class_ID, age)

    if annual_vmt_id in vmt_dict and not query:
        annual_vmt = vmt_dict[annual_vmt_id]
    else:
        annual_vmt = float(o2.session.query(o2.options.stock_vmt.annual_vmt). \
            filter(o2.options.stock_vmt.market_class_ID == market_class_ID). \
            filter(o2.options.stock_vmt.age == age).scalar())

        vmt_dict[annual_vmt_id] = annual_vmt

    return annual_vmt


scrappage_dict = dict()
def get_scrappage_factor(calendar_year, market_class_ID, model_year, query=False):
    # get scrappage factor
    age = (calendar_year - model_year)

    scrappage_factor_id = '%s_%s' % (market_class_ID, age)

    if scrappage_factor_id in scrappage_dict and not query:
        scrappage_factor = scrappage_dict[scrappage_factor_id]
    else:
        scrappage_factor = float(o2.session.query(o2.options.stock_scrappage.reregistered_proportion). \
                                filter(o2.options.stock_scrappage.market_class_ID == market_class_ID). \
                                filter(o2.options.stock_scrappage.age == age).scalar())
        scrappage_dict[scrappage_factor_id] = scrappage_factor

    return scrappage_factor


vehicles_dict = dict()
def get_vehicle_info(vehicle_ID, query=False):
    from vehicles import VehicleFinal

    if vehicle_ID in vehicles_dict and not query:
        market_class_ID, model_year, initial_registered_count = vehicles_dict[vehicle_ID]
    else:
        market_class_ID, model_year, initial_registered_count = \
            o2.session.query(VehicleFinal.market_class_ID, VehicleFinal.model_year, VehicleFinal._initial_registered_count).\
            filter(VehicleFinal.vehicle_ID == vehicle_ID).one()
        vehicles_dict[vehicle_ID] = market_class_ID, model_year, initial_registered_count

    return market_class_ID, model_year, initial_registered_count


def update_stock(calendar_year):
    """
    Deregister vehicles by calendar year, as a function of vehicle attributes (e.g. age, market class...)
    Update VMT
    :param calendar_year: calendar year
    :return: updates vehicle annual data table
    """
    query = False

    from vehicles import VehicleFinal
    from vehicle_annual_data import VehicleAnnualData

    # pull in this year's vehicle ids:
    this_years_vehicle_annual_data = VehicleAnnualData.get_vehicle_annual_data(calendar_year)

    o2.session.add_all(this_years_vehicle_annual_data)
    # UPDATE vehicle annual data for this year's stock
    for vad in this_years_vehicle_annual_data:
        market_class_ID, model_year, initial_registered_count = get_vehicle_info(vad.vehicle_ID, query=query)

        scrappage_factor = get_scrappage_factor(calendar_year, market_class_ID, model_year, query=query)

        annual_vmt = get_annual_vmt(calendar_year, market_class_ID, model_year, query=query)

        registered_count = initial_registered_count * scrappage_factor

        vad.annual_vmt = annual_vmt
        vad.vmt = annual_vmt * registered_count

    prior_year_vehicle_ids = sql_unpack_result(VehicleAnnualData.get_vehicle_annual_data(calendar_year-1, 'vehicle_ID'))

    vad_list = []

    # CREATE vehicle annual data for last year's stock, now one year older:
    if prior_year_vehicle_ids:
        for vehicle_ID in prior_year_vehicle_ids:
            market_class_ID, model_year, initial_registered_count = get_vehicle_info(vehicle_ID, query=query)

            scrappage_factor = get_scrappage_factor(calendar_year, market_class_ID, model_year, query=query)

            annual_vmt = get_annual_vmt(calendar_year, market_class_ID, model_year, query=query)

            registered_count = initial_registered_count * scrappage_factor

            vad_list.append(VehicleAnnualData(vehicle_ID=vehicle_ID,
                                              calendar_year=calendar_year,
                                              registered_count=registered_count,
                                              age=calendar_year-model_year,
                                              annual_vmt=annual_vmt,
                                              vmt=annual_vmt * registered_count)
                            )

    o2.session.add_all(vad_list)


if __name__ == '__main__':
    try:
        if '__file__' in locals():
            print(fileio.get_filenameext(__file__))

        # from usepa_omega2 import *
        # from usepa_omega2.manufacturers import Manufacturer  # required by vehicles
        # from usepa_omega2.fuels import Fuel  # required by vehicles
        # from usepa_omega2.market_classes import MarketClass  # required by vehicles
        # # from vehicles import Vehicle  # for foreign key vehicle_ID
        #
        # fuels_file = 'EPA_OMEGA_MODEL/test_inputs/fuels.csv'
        # self.manufacturers_file = 'test_inputs/manufacturers.csv'
        # self.market_classes_file = 'test_inputs/market_classes.csv'
        # self.vehicles_file = 'test_inputs/vehicles.csv'
        #
        # # session = Session(bind=engine)
        # SQABase.metadata.create_all(engine)
        #
        # init_fail = []
        # init_fail = init_fail + MarketClass.init_database_from_file(o2_options.market_classes_file, session, verbose=o2_options.verbose)
        # init_fail = init_fail + Fuel.init_database_from_file(o2_options.fuels_file, session, verbose=o2_options.verbose)
        # init_fail = init_fail + Manufacturer.init_database_from_file(o2_options.manufacturers_file, session, verbose=o2_options.verbose)
        #
        # if not init_fail:
        #     for yr in (o2_options.analysis_initial_year, o2_options.analysis_final_year + 1):
        #         calc_stock_registered_count(session, yr)
        #     dump_database_to_csv(engine, o2_options.database_dump_folder, verbose=o2_options.verbose)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
