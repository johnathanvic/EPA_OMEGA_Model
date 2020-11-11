"""
emission_costs_criteria.py
=============================


"""

import o2  # import global variables
from usepa_omega2 import *
import pandas as pd
import numpy as np
from pathlib import Path

# path_code = Path(__file__).parent
path_project = Path.cwd()
path_input_samples = path_project / 'input_samples'
deflators = pd.read_csv(path_input_samples / 'price_deflators.csv', skiprows=1, index_col=0) # for now, but CPU deflators should be used for these


def adjust_dollars(df, deflators, *args):
    basis_years = df['dollar_basis'].unique()
    df_return = df.copy()
    for basis_year in basis_years:
        for arg in args:
            adj_factor = deflators.at[basis_year, 'adjustment_factor']
            df_return.loc[df_return['dollar_basis'] == basis_year, arg] = df_return[arg] * adj_factor
    df_return['dollar_basis'] = deflators.index[deflators['adjustment_factor'] == 1][0]
    return df_return


class EmissionCostsCriteria(SQABase):
    # --- database table properties ---
    __tablename__ = 'emission_costs_criteria'
    index = Column('index', Integer, primary_key=True)

    calendar_year = Column('calendar_year', Numeric)
    discount_rate = Column('discount_rate', Numeric)
    fuel_id = Column('fuel_id', String)
    pollutant = Column('pollutant', String)
    dollar_basis = Column('dollar_basis', Numeric)
    low_mortality_onroad = Column('low-mortality_onroad', Numeric)
    high_mortality_onroad = Column('high-mortality_onroad', Numeric)
    low_mortality_upstream = Column('low-mortality_upstream', Numeric)
    high_mortality_upstream = Column('high-mortality_upstream', Numeric)

    def __repr__(self):
        return f"<OMEGA2 {type(self).__name__} object at 0x{id(self)}>"

    @staticmethod
    def init_database_from_file(filename, verbose=False):
        if verbose:
            omega_log.logwrite(f'\nInitializing database from {filename}...')

        input_template_name = 'emission_costs-criteria'
        input_template_version = 0.1
        input_template_columns = {'calendar_year', 'discount_rate', 'fuel_id', 'pollutant', 'dollar_basis',
                                  'low-mortality_onroad', 'high-mortality_onroad',
                                  'low-mortality_upstream', 'high-mortality_upstream'}

        template_errors = validate_template_version_info(filename, input_template_name, input_template_version,
                                                         verbose=verbose)

        if not template_errors:
            # read in the data portion of the input file
            df = pd.read_csv(filename, skiprows=1)
            df = df.loc[df['dollar_basis'] != 0, :]
            template_errors = validate_template_columns(filename, input_template_columns, df.columns, verbose=verbose)

            df = adjust_dollars(df, deflators, 'low-mortality_onroad', 'high-mortality_onroad', 'low-mortality_upstream', 'high-mortality_upstream')

            if not template_errors:
                obj_list = []
                # load data into database
                for i in df.index:
                    obj_list.append(EmissionCostsCriteria(
                        calendar_year=df.loc[i, 'calendar_year'],
                        discount_rate=df.loc[i, 'discount_rate'],
                        fuel_id=df.loc[i, 'fuel_id'],
                        pollutant=df.loc[i, 'pollutant'],
                        dollar_basis=df.loc[i, 'dollar_basis'],
                        low_mortality_onroad=df.loc[i, 'low-mortality_onroad'],
                        high_mortality_onroad=df.loc[i, 'high-mortality_onroad'],
                        low_mortality_upstream=df.loc[i, 'low-mortality_upstream'],
                        high_mortality_upstream=df.loc[i, 'high-mortality_upstream'],
                    ))
                o2.session.add_all(obj_list)
                o2.session.flush()

        return template_errors


if __name__ == '__main__':
    try:
        if '__file__' in locals():
            print(fileio.get_filenameext(__file__))

        # set up global variables:
        o2.options = OMEGARuntimeOptions()
        init_omega_db()
        omega_log.init_logfile()

        from usepa_omega2.market_classes import MarketClass  # needed for market class ID

        SQABase.metadata.create_all(o2.engine)

        init_fail = []
        # init_fail = init_fail + MarketClass.init_database_from_file(o2.options.market_classes_file,
        #                                                             verbose=o2.options.verbose)

        init_fail = init_fail + EmissionCostsCriteria.init_database_from_file(o2.options.criteria_costs_file,
                                                                              verbose=o2.options.verbose)

        if not init_fail:
            dump_omega_db_to_csv(o2.options.database_dump_folder)
        else:
            print(init_fail)
            print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
            os._exit(-1)

    except:
        print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
        os._exit(-1)
