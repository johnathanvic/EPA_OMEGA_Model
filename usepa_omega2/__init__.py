"""
__init.py__
===========


"""

# OMEGA2 code version number
code_version = "0.3.0"
print('loading usepa_omega2 version %s' % code_version)

import os, traceback

try:
    import pandas as pd
    pd.set_option('chained_assignment', 'raise')

    from o2 import OMEGABase
    from omega_db import *
    from omega_types import *
    import omega_log
    import file_eye_oh as fileio
    from input_validation import *
    from omega_functions import *

    import scipy.interpolate

    # --- OMEGA2 global constants ---

    # enumerated values
    fueling_classes = OMEGAEnum(['BEV', 'ICE'])
    hauling_classes = OMEGAEnum(['hauling', 'non hauling'])
    ownership_classes = OMEGAEnum(['shared', 'private'])
    reg_classes = OMEGAEnum(['car', 'truck'])
    fuel_units = OMEGAEnum(['gallon', 'kWh'])

    class OMEGARuntimeOptions(OMEGABase):
        def __init__(self):
            import time

            self.session_name = 'OMEGA2 Demo'
            self.session_unique_name = 'OMEGA2 Demo'
            self.verbose = False
            self.output_folder = 'output' + os.sep
            self.database_dump_folder = self.output_folder + '__dump' + os.sep
            self.manufacturers_file = 'input_samples/manufacturers.csv'
            self.market_classes_file = 'input_samples/market_classes.csv'
            self.vehicles_file = 'input_samples/vehicles.csv'
            self.demanded_shares_file = 'input_samples/demanded_shares-gcam.csv'
            self.fuels_file = 'input_samples/fuels.csv'
            self.context_folder = ''
            self.context_id = 'AEO2020'
            self.context_case_id = 'Reference case'
            self.context_fuel_prices_file = 'input_samples/context_fuel_prices.csv'
            self.context_fuel_upstream_file = 'input_samples/context_fuel_upstream.csv'
            self.context_new_vehicle_market_file = 'input_samples/context_new_vehicle_market.csv'
            self.cost_file = 'input_samples/cost_curves.csv'
            self.cost_curve_frontier_affinity_factor = 0.75
            self.analysis_initial_year = None
            self.analysis_final_year = None
            self.logfile_prefix = 'o2log_'
            self.logfilename = ''
            self.producer_calculate_generalized_cost = None
            self.consumer_calculate_generalized_cost = None
            self.ghg_standards_file = 'input_samples/ghg_standards-flat.csv'
            self.ghg_standards_fuels_file = 'input_samples/ghg_standards-fuels.csv'
            self.required_zev_share_file = 'input_samples/required_zev_share.csv'
            self.reregistration_fixed_by_age_file = 'input_samples/reregistration_fixed_by_age.csv'
            self.annual_vmt_fixed_by_age_file = 'input_samples/annual_vmt_fixed_by_age.csv'
            self.slice_tech_combo_cloud_tables = False

            self.allow_backsliding = True

            self.producer_max_iterations = 15
            self.producer_num_market_share_options = 5
            self.producer_num_tech_options_per_ice_vehicle = 5
            self.producer_num_tech_options_per_bev_vehicle = 1
            self.producer_iteration_tolerance = 1e-6

            self.iterate_producer_consumer = True
            self.producer_consumer_max_iterations = 10
            self.producer_consumer_iteration_tolerance = 0.01

            self.consumer_pricing_max_iterations = 50
            self.consumer_pricing_num_options = 4
            self.consumer_pricing_multiplier_min = 0.8
            self.consumer_pricing_multiplier_max = 1.2

            self.new_vehicle_sales_response_elasticity = -0.5
            self.timestamp_str = time.strftime('%Y%m%d_%H%M%S')

            self.calc_effects = True
            # effects modeling files
            self.ip_deflators_file = 'input_samples/context_implicit_price_deflators.csv'
            self.cpi_deflators_file = 'input_samples/context_cpi_price_deflators.csv'
            self.scc_cost_factors_file = 'input_samples/context_cost_factors-scc.csv'
            self.criteria_cost_factors_file = 'input_samples/context_cost_factors-criteria.csv'
            self.emission_factors_vehicles_file = 'input_samples/context_emission_factors-vehicles.csv'
            self.emission_factors_powersector_file = 'input_samples/context_emission_factors-powersector.csv'
            self.emission_factors_refinery_file = 'input_samples/context_emission_factors-refinery.csv'

            self.start_time = 0
            self.end_time = 0

            # debugging options
            self.verbose_console = []  # ['producer', 'consumer']  # list of modules to allow verbose console output, or empty to disable
            self.run_profiler = False
            self.flat_context = False
            self.flat_context_year = 2021
            self.num_analysis_years = 1  # number of years to run, if not all (None = run all)
            self.log_producer_iteration_years = []  # = 'all' or list of years to log, empty list to disable logging
            self.log_consumer_iteration_years = [2050]  # = 'all' or list of years to log, empty list to disable logging
            self.log_sales_demand_years = []  # [2029]  # 'all'  # = 'all' or list of years to log, empty list to disable logging

    from omega2 import run_omega

except:
    print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
    os._exit(-1)
