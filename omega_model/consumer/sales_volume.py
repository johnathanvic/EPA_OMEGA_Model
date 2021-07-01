"""

Consumer module stub (for now)


----

**CODE**

"""

from omega_model import *


# placeholder for consumer generalized vehicle cost:
def calc_generalized_cost(cost_factors):
    pass


def context_new_vehicle_sales(model_year):
    """
    :param model_year: not used, for now
    :return: dict of sales by consumer (market) categories
    """

    #  PHASE0: hauling/non, EV/ICE, We don't need shared/private for beta
    from context.new_vehicle_market import NewVehicleMarket

    sales_dict = dict()

    if omega_globals.options.flat_context:
        model_year = omega_globals.options.flat_context_year

    # get total sales from context
    total_sales = NewVehicleMarket.new_vehicle_sales(model_year)

    # pulling in hauling sales, non_hauling = total minus hauling
    hauling_sales = 0
    for hsc in NewVehicleMarket.hauling_context_size_class_info:
        hauling_sales += NewVehicleMarket.new_vehicle_sales(model_year, context_size_class=hsc) * \
                         NewVehicleMarket.hauling_context_size_class_info[hsc]['hauling_share']

    sales_dict['hauling'] = hauling_sales
    sales_dict['non_hauling'] = total_sales - hauling_sales
    sales_dict['total'] = total_sales

    return sales_dict


def new_vehicle_sales_response(calendar_year, P):
    """
    Calculate new vehicle sales, relative to a reference sales volume and average new vehicle price
    :param P: a single price or a list-like of prices
    :return: total new vehicle sales volume at each price
    """
    from context.new_vehicle_market import NewVehicleMarket

    if type(P) is list:
        import numpy as np
        P = np.array(P)

    if omega_globals.options.session_is_reference and isinstance(P, float):
        NewVehicleMarket.set_new_vehicle_generalized_cost(calendar_year, P)

    Q0 = NewVehicleMarket.new_vehicle_sales(calendar_year)
    P0 = NewVehicleMarket.new_vehicle_generalized_cost(calendar_year)

    E = omega_globals.options.new_vehicle_sales_response_elasticity

    M = -(Q0*E - Q0) / (P0/E - P0)  # slope of linear response

    Q = Q0 + M * (P-P0)  # point-slope equation of a line

    return Q


if __name__ == '__main__':
    try:
        if '__file__' in locals():
            print(file_io.get_filenameext(__file__))

        # set up global variables:
        omega_globals.options = OMEGARuntimeOptions()
        init_omega_db()
        omega_log.init_logfile()

        init_fail = []

        from producer.vehicles import VehicleFinal
        from producer.vehicle_annual_data import VehicleAnnualData
        from producer.manufacturers import Manufacturer  # needed for manufacturers table
        from consumer.market_classes import MarketClass  # needed for market class ID
        from context.onroad_fuels import OnroadFuel  # needed for showroom fuel ID
        from context.cost_clouds import CostCloud  # needed for vehicle cost from CO2
        from context.new_vehicle_market import NewVehicleMarket

        from policy.targets_flat import input_template_name as flat_template_name
        from policy.targets_footprint import input_template_name as footprint_template_name
        ghg_template_name = get_template_name(omega_globals.options.ghg_standards_file)

        if ghg_template_name == flat_template_name:
            from policy.targets_flat import TargetsFlat

            omega_globals.options.GHG_standard = TargetsFlat
        elif ghg_template_name == footprint_template_name:
            from policy.targets_footprint import TargetsFootprint

            omega_globals.options.GHG_standard = TargetsFootprint
        else:
            init_fail.append('UNKNOWN GHG STANDARD "%s"' % ghg_template_name)

        SQABase.metadata.create_all(omega_globals.engine)

        init_fail += Manufacturer.init_database_from_file(omega_globals.options.manufacturers_file,
                                                          verbose=omega_globals.options.verbose)
        init_fail += MarketClass.init_database_from_file(omega_globals.options.market_classes_file,
                                                         verbose=omega_globals.options.verbose)
        init_fail += OnroadFuel.init_from_file(omega_globals.options.onroad_fuels_file, verbose=omega_globals.options.verbose)

        init_fail += CostCloud.init_cost_clouds_from_file(omega_globals.options.cost_file, verbose=omega_globals.options.verbose)

        init_fail += omega_globals.options.GHG_standard.init_database_from_file(omega_globals.options.ghg_standards_file,
                                                                                verbose=omega_globals.options.verbose)

        init_fail += VehicleFinal.init_database_from_file(omega_globals.options.vehicles_file,
                                                          omega_globals.options.vehicle_onroad_calculations_file,
                                                          verbose=omega_globals.options.verbose)

        init_fail += NewVehicleMarket.init_database_from_file(
            omega_globals.options.context_new_vehicle_market_file, verbose=omega_globals.options.verbose)

        if not init_fail:
            omega_globals.options.analysis_initial_year = VehicleFinal.get_max_model_year() + 1

            sales_demand = context_new_vehicle_sales(omega_globals.options.analysis_initial_year)
        else:
            print(init_fail)
            print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
            os._exit(-1)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
