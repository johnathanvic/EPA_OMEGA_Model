"""

Vehicle re-registration, fixed by age.

**INPUT FILE FORMAT**

The file format consists of a one-row template header followed by a one-row data header and subsequent data
rows.  The template header uses a dynamic format.

The data represents the re-registered proportion of vehicles by age and market class.

File Type
    comma-separated values (CSV)

Template Header
    .. csv-table::

       input_template_name:,``[module_name]``,input_template_version:,0.1

Sample Header
    .. csv-table::

       input_template_name:, consumer.reregistration_fixed_by_age, input_template_version:, 0.1

Sample Data Columns
    .. csv-table::
        :widths: auto

        age,market_class_id,reregistered_proportion,
        0,non_hauling.BEV,1,
        1,non_hauling.BEV,0.987841531,
        2,non_hauling.BEV,0.976587217,
        0,hauling.ICE,1,
        1,hauling.ICE,0.977597055,
        2,hauling.ICE,0.962974697,

Data Column Name and Description

:age:
    Vehicle age, in years

:market_class_id:
    Vehicle market class ID, e.g. 'hauling.ICE'

:reregistered_proportion:
    The fraction of vehicles re-registered, [0..1]

----

**CODE**


"""

from omega_model import *


class Reregistration(OMEGABase, ReregistrationBase):
    """
    **Load and provide access to vehicle re-registration data.**
    """

    _data = dict()

    @staticmethod
    def get_reregistered_proportion(market_class_id, age):
        """
        Get vehicle re-registered proportion [0..1] by market class and age.

        Args:
            market_class_id (str): market class id, e.g. 'hauling.ICE'
            age (int): vehicle age

        Returns:
            Re-registered proportion [0..1]

        """
        return Reregistration._data[market_class_id, age]['reregistered_proportion']

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
        Reregistration._data.clear()

        if verbose:
            omega_log.logwrite(f'\nInitializing database from {filename}...')

        input_template_name = __name__
        input_template_version = 0.1
        input_template_columns = {'age', 'market_class_id', 'reregistered_proportion'}

        template_errors = validate_template_version_info(filename, input_template_name, input_template_version,
                                                         verbose=verbose)

        if not template_errors:
            # read in the data portion of the input file
            df = pd.read_csv(filename, skiprows=1)

            template_errors = validate_template_columns(filename, input_template_columns, df.columns, verbose=verbose)

            if not template_errors:
                # validate data
                for i in df.index:
                    template_errors += \
                        omega_globals.options.MarketClass.validate_market_class_id(df.loc[i, 'market_class_id'])

            if not template_errors:
                Reregistration._data = df.set_index(['market_class_id', 'age']).sort_index().to_dict(orient='index')

        return template_errors


if __name__ == '__main__':

    __name__ = '%s.%s' % (file_io.get_parent_foldername(__file__), file_io.get_filename(__file__))

    try:
        if '__file__' in locals():
            print(file_io.get_filenameext(__file__))

        import importlib

        omega_globals.options = OMEGASessionSettings()
        omega_log.init_logfile()

        init_fail = []

        # pull in reg classes before initializing classes that check reg class validity
        module_name = get_template_name(omega_globals.options.policy_reg_classes_file)
        omega_globals.options.RegulatoryClasses = importlib.import_module(module_name).RegulatoryClasses
        init_fail += omega_globals.options.RegulatoryClasses.init_from_file(
            omega_globals.options.policy_reg_classes_file)

        # pull in market classes before initializing classes that check market class validity
        module_name = get_template_name(omega_globals.options.market_classes_file)
        omega_globals.options.MarketClass = importlib.import_module(module_name).MarketClass
        init_fail += omega_globals.options.MarketClass.init_from_file(omega_globals.options.market_classes_file,
                                                verbose=omega_globals.options.verbose)

        init_fail += Reregistration.init_from_file(
            omega_globals.options.vehicle_reregistration_file, verbose=omega_globals.options.verbose)

        if not init_fail:
            pass
        else:
            print(init_fail)
            print("\n#INIT FAIL\n%s\n" % traceback.format_exc())
            os._exit(-1)
    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
