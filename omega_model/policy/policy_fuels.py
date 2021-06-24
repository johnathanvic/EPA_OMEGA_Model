"""

**Routines to load and provide access to policy-defined fuel attributes.**

The primary fuel attribute is CO2 grams per unit (i.e. g/gallon, g/kWh) when consumed, by policy year.


----

**INPUT FILE FORMAT**

The file format consists of a one-row template header followed by a one-row data header and subsequent data
rows.

The data represents fuel property data for compliance purposes, by policy year.

File Type
    comma-separated values (CSV)

Template Header
    .. csv-table::

       input_template_name:,ghg_standards-fuels,input_template_version:,0.1

Sample Data Columns
    .. csv-table::
        :widths: auto

        fuel_id,start_year,cert_co2_grams_per_unit
        US electricity,2020,534
        gasoline,2020,8887

Data Column Name and Description

:fuel_id:
    The Fuel ID, as referenced by the ``policy_fuel_upstream`` module.

:start_year:
    Start year of fuel properties, properties apply until the next available start year

:cert_co2_grams_per_unit:
    CO2 emissions per unit when consumed, for compliance purposes

----

**CODE**

"""

print('importing %s' % __file__)

from omega_model import *

cache = dict()


class PolicyFuel(OMEGABase):
    """
    **Loads and provides methods to access onroad fuel attribute data.**

    """

    @staticmethod
    def get_fuel_attribute(calendar_year, fuel_id, attribute):
        """

        Args:
            calendar_year (numeric): year to get fuel properties in
            fuel_id (str): e.g. 'pump gasoline')
            attribute (str): name of attribute to retrieve

        Returns:
            Fuel attribute value for the given year.

        Example:

            ::

                carbon_intensity_gasoline =
                    OnroadFuel.get_fuel_attribute(2020, 'pump gasoline', 'direct_co2_grams_per_unit')

        """
        start_years = cache['start_year']
        if start_years[start_years <= calendar_year]:
            cache_key = max(start_years[start_years <= calendar_year])

        return cache[cache_key][fuel_id][attribute]

    @staticmethod
    def validate_fuel_ID(fuel_id):
        """
        Validate fuel ID

        Args:
            fuel_id (str): e.g. 'pump gasoline')

        Returns:
            True if the fuel ID is valid, False otherwise

        """
        return fuel_id in cache['fuel_id']

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
        import numpy as np

        cache.clear()

        if verbose:
            omega_log.logwrite('\nInitializing database from %s...' % filename)

        input_template_name = 'policy-fuels'
        input_template_version = 0.1
        input_template_columns = {'fuel_id', 'start_year', 'unit', 'direct_co2_grams_per_unit',
                                  'upstream_co2_grams_per_unit', 'transmission_efficiency'}

        template_errors = validate_template_version_info(filename, input_template_name, input_template_version,
                                                         verbose=verbose)

        if not template_errors:
            # read in the data portion of the input file
            df = pd.read_csv(filename, skiprows=1)

            template_errors = validate_template_columns(filename, input_template_columns, df.columns, verbose=verbose)

            if not template_errors:
                df = df.set_index('start_year')

                for idx, r in df.iterrows():
                    if idx not in cache:
                        cache[idx] = dict()

                    cache[idx][r.fuel_id] = r.to_dict()

                cache['start_year'] = np.array(list(cache.keys()))
                cache['fuel_id'] = np.array(list(df['fuel_id'].unique()))

        return template_errors


if __name__ == '__main__':
    try:
        import os

        if '__file__' in locals():
            print(file_io.get_filenameext(__file__))

        # set up global variables:
        omega_globals.options = OMEGARuntimeOptions()
        init_omega_db()
        omega_globals.engine.echo = omega_globals.options.verbose
        omega_log.init_logfile()

        init_fail = []
        init_fail += PolicyFuel.init_from_file(omega_globals.options.policy_fuels_file, verbose=omega_globals.options.verbose)

        if not init_fail:
            print(PolicyFuel.validate_fuel_ID('gasoline'))
            print(PolicyFuel.get_fuel_attribute(2020, 'gasoline', 'direct_co2_grams_per_unit'))
            print(PolicyFuel.get_fuel_attribute(2020, 'electricity', 'transmission_efficiency'))
        else:
            print(init_fail)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
