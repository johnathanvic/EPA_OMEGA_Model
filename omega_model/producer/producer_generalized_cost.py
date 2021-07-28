"""

**Routines to implement producer generalized cost calculations.**

**INPUT FILE FORMAT**

The file format consists of a one-row template header followed by a one-row data header and subsequent data
rows.

The data represents producer generalized cost parameters by market class ID.

File Type
    comma-separated values (CSV)

Template Header
    .. csv-table::

       input_template_name:,producer_generalized_cost,input_template_version:,0.1

Sample Data Columns
    .. csv-table::
        :widths: auto

        market_class_id,fuel_years,annual_vmt
        non_hauling.BEV,5,15000
        hauling.ICE,5,15000

Data Column Name and Description

:market_class_id:
    Vehicle market class ID, e.g. 'hauling.ICE'

:fuel_years:
    Number of years of fuel cost to include in producer generalized cost

:annual_vmt:
    Annual vehicle miles travelled for calculating producer generalized cost

----

**CODE**

"""

print('importing %s' % __file__)

from omega_model import *


cache = dict()


class ProducerGeneralizedCost(OMEGABase, SQABase, ProducerGeneralizedCostBase):
    """
    Loads producer generalized cost data and provides cost calculation functionality.

    """
    # --- database table properties ---
    __tablename__ = 'producer_generalized_cost'
    market_class_id = Column('market_class_id', String, primary_key=True)  #: market class id, e.g. 'non_hauling.ICE'
    fuel_years = Column(Float)  #: years of fuel consumption, for producer generalized cost calcs
    annual_vmt = Column(Float)  #: annual vehicle miles travelled, for producer generalized cost calcs

    @staticmethod
    def get_producer_generalized_cost_attributes(market_class_id, attribute_types):
        """
        Get one or more producer generalized cost attributes associated with the given market class ID.

        Args:
            market_class_id (str): e.g. 'hauling.ICE'
            attribute_types (str, [strs]): name or list of generalized cost attribute(s), e.g. ``['producer_generalized_cost_fuel_years', 'producer_generalized_cost_annual_vmt']``

        Returns:
            The requested generalized cost attributes.

        """
        cache_key = '%s_%s' % (market_class_id, attribute_types)

        if cache_key not in cache:
            if type(attribute_types) is not list:
                attribute_types = [attribute_types]

            attrs = ProducerGeneralizedCost.get_class_attributes(attribute_types)

            result = omega_globals.session.query(*attrs). \
                filter(ProducerGeneralizedCost.market_class_id == market_class_id).all()[0]

            if len(attribute_types) == 1:
                cache[cache_key] = result[0]
            else:
                cache[cache_key] = result

        return cache[cache_key]

    @staticmethod
    def calc_generalized_cost(vehicle, co2_name, kwh_name, cost_name):
        """

        Args:
            vehicle:
            co2_name:
            kwh_name:
            cost_name:

        Returns:
            A cost curve modified by generalized cost factors

        """

        from context.price_modifications import PriceModifications
        from context.onroad_fuels import OnroadFuel

        producer_generalized_cost_fuel_years, producer_generalized_cost_annual_vmt = \
            ProducerGeneralizedCost. \
                get_producer_generalized_cost_attributes(vehicle.market_class_id, ['fuel_years', 'annual_vmt'])

        cost_cloud = vehicle.cost_cloud
        vehicle_cost = cost_cloud[cost_name]
        vehicle_co2e_grams_per_mile = cost_cloud[co2_name]
        vehicle_direct_kwh_per_mile = cost_cloud[kwh_name] / OnroadFuel.get_fuel_attribute(vehicle.model_year,
                                                                                           'US electricity',
                                                                                           'refuel_efficiency')

        price_modification = PriceModifications.get_price_modification(vehicle.model_year, vehicle.market_class_id)

        grams_co2e_per_unit = vehicle.onroad_co2e_emissions_grams_per_unit()
        liquid_generalized_fuel_cost = 0
        electric_generalized_fuel_cost = 0

        if grams_co2e_per_unit > 0:
            liquid_generalized_fuel_cost = \
                (vehicle.retail_fuel_price_dollars_per_unit(vehicle.model_year) / grams_co2e_per_unit *
                 vehicle_co2e_grams_per_mile *
                 producer_generalized_cost_annual_vmt *
                 producer_generalized_cost_fuel_years)

        if any(vehicle_direct_kwh_per_mile > 0):
            electric_generalized_fuel_cost = (vehicle_direct_kwh_per_mile *
                                              vehicle.retail_fuel_price_dollars_per_unit(vehicle.model_year) *
                                              producer_generalized_cost_annual_vmt * producer_generalized_cost_fuel_years)

        generalized_fuel_cost = liquid_generalized_fuel_cost + electric_generalized_fuel_cost

        cost_cloud[
            cost_name.replace('mfr', 'mfr_generalized')] = generalized_fuel_cost + vehicle_cost + price_modification

        return cost_cloud

    @staticmethod
    def init_from_file(filename, verbose=False):
        """

        Initialize class data from input file.

        Args:
            filename (str): name of input file
            verbose (bool): enable additional console and logfile output if True

        Returns:
            List of template/input errors, else empty list on success

        """
        cache.clear()

        if verbose:
            omega_log.logwrite('\nInitializing database from %s...' % filename)

        input_template_name = __name__
        input_template_version = 0.1
        input_template_columns = {'market_class_id', 'fuel_years', 'annual_vmt'}

        template_errors = validate_template_version_info(filename, input_template_name, input_template_version, verbose=verbose)

        if not template_errors:
            # read in the data portion of the input file
            df = pd.read_csv(filename, skiprows=1)

            template_errors = validate_template_columns(filename, input_template_columns, df.columns, verbose=verbose)

            if not template_errors:
                obj_list = []
                # load data into database
                for i in df.index:
                    obj_list.append(ProducerGeneralizedCost(
                        market_class_id=df.loc[i, 'market_class_id'],
                        fuel_years=df.loc[i, 'fuel_years'],
                        annual_vmt=df.loc[i, 'annual_vmt'],
                    ))
                omega_globals.session.add_all(obj_list)
                omega_globals.session.flush()

        return template_errors


if __name__ == '__main__':

    __name__ = 'producer.producer_generalized_cost'

    try:
        if '__file__' in locals():
            print(file_io.get_filenameext(__file__))

        import importlib

        # set up global variables:
        omega_globals.options = OMEGASessionSettings()

        init_fail = []

        # pull in reg classes before building database tables (declaring classes) that check reg class validity
        module_name = get_template_name(omega_globals.options.policy_reg_classes_file)
        omega_globals.options.RegulatoryClasses = importlib.import_module(module_name).RegulatoryClasses
        init_fail += omega_globals.options.RegulatoryClasses.init_from_file(
            omega_globals.options.policy_reg_classes_file)


        init_omega_db(omega_globals.options.verbose)
        omega_log.init_logfile()

        SQABase.metadata.create_all(omega_globals.engine)

        init_fail = []
        init_fail += ProducerGeneralizedCost.init_database_from_file(
            omega_globals.options.producer_generalized_cost_file, verbose=omega_globals.options.verbose)

        if not init_fail:
            from common.omega_functions import print_dict

            dump_omega_db_to_csv(omega_globals.options.database_dump_folder)

        else:
            print(init_fail)
            print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
            os._exit(-1)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)