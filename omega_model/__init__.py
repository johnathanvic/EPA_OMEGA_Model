"""

Top-level includes/definitions for the OMEGA model

Defines class OMEGASessionSettings which control an individual simulation session


----

**CODE**

"""

# OMEGA code version number
code_version = "2.1.0"
print('loading omega version %s' % code_version)

import os, sys

if 'darwin' in sys.platform:
    os.environ['QT_MAC_WANTS_LAYER'] = '1'  # for pyqtgraph on MacOS

# CU

import traceback

try:
    import time

    import pandas as pd
    # from warnings import simplefilter
    # simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
    pd.set_option('chained_assignment', 'raise')
    from pandas.api.types import is_numeric_dtype

    import numpy as np
    import copy

    from common.omega_globals import *
    from common.omega_types import *
    from common.omega_db import *
    from common import file_io, omega_log
    from common.input_validation import *
    from common.omega_functions import *
    from common.omega_eval import *
    from context.context_base_classes import *
    from context.onroad_fuels import *
    from policy.policy_base_classes import *
    from consumer.consumer_base_classes import *
    from producer.producer_base_classes import *

    # --- OMEGA2 global constants ---

    # enumerated values
    fueling_classes = OMEGAEnum(['BEV', 'ICE'])
    ownership_classes = OMEGAEnum(['shared', 'private'])
    legacy_reg_classes = OMEGAEnum(['car', 'truck', 'mediumduty'])
    fuel_units = OMEGAEnum(['gallon', 'kWh'])

    class OMEGASessionSettings(OMEGABase):
        """
        Define the settings required for a simulation session

        """
        def __init__(self):
            """
            Create an OMEGASessionSettings object with default settings used for testing and development.

            The primary way to create an OMEGASessionSettings object is via the batch process.

            See Also:
                omega_batch.py

            """
            import time

            path = os.path.dirname(os.path.abspath(__file__)) + os.sep
            # inputs_folder = 'proposal_inputs/'
            self.inputfile_metadata = []
            self.session_name = 'OMEGA Quick Test'
            self.session_unique_name = 'OMEGA Quick Test'
            self.session_is_reference = True
            self.auto_close_figures = True
            self.save_preliminary_outputs = True
            self.output_folder_base = 'out' + os.sep
            self.output_folder = self.output_folder_base
            self.database_dump_folder = self.output_folder + '__dump' + os.sep
            self.omega_model_path = path
            self.use_prerun_context_outputs = False
            self.prerun_context_folder = ''
            self.credit_market_efficiency = 1.0
            self.consolidate_manufacturers = None
            self.force_two_pass = False
            self.include_manufacturers_list = 'all'
            self.exclude_manufacturers_list = 'none'
            self.manufacturers_file = path + 'proposal_inputs/manufacturers_20220329.csv'
            self.vehicles_file = path + 'proposal_inputs/vehicles_ldv_20221017_cleanedredesigne.csv'
            self.vehicles_file_base_year = None
            self.vehicles_df = pd.DataFrame()
            self.onroad_vehicle_calculations_file = path + 'proposal_inputs/onroad_vehicle_calculations_20221028a.csv'
            self.onroad_fuels_file = path + 'proposal_inputs/onroad_fuels_20220325.csv'
            self.context_id = 'AEO2021'
            self.context_case_id = 'Reference case'
            self.context_new_vehicle_generalized_costs_file = None
            self.sales_share_calibration_file = None
            self.generate_context_calibration_files = True
            self.context_fuel_prices_file = path + 'proposal_inputs/context_fuel_prices_20220429.csv'
            self.fuel_upstream_methods_file = path + 'proposal_inputs/policy_fuel_upstream_methods-upstream_zero_20210602.csv'
            self.drive_cycles_file = path + 'proposal_inputs/drive_cycles_20220325.csv'
            self.drive_cycle_weights_file = path + 'proposal_inputs/drive_cycle_weights_5545_20220518.csv'
            self.drive_cycle_ballast_file = path + 'proposal_inputs/drive_cycle_ballast_20220325.csv'
            self.context_stock_vmt_file = path + 'proposal_inputs/context_stock_vmt_20221031.csv'

            self.ice_vehicle_simulation_results_file = path + 'proposal_inputs/simulated_vehicles_rse_ice_20221021_debug_noP2.csv'
            self.bev_vehicle_simulation_results_file = path + 'proposal_inputs/simulated_vehicles_rse_bev_20221101.csv'
            self.phev_vehicle_simulation_results_file = path + 'proposal_inputs/simulated_vehicles_rse_phev_20220711.csv'

            self.powertrain_cost_input_file = path + 'proposal_inputs/powertrain_cost_20230314.csv'
            self.glider_cost_input_file = path + 'proposal_inputs/glider_cost_20220719.csv'
            self.body_styles_file = path + 'proposal_inputs/body_styles_20220324.csv'
            self.mass_scaling_file = path + 'proposal_inputs/mass_scaling_20220719.csv'

            self.analysis_initial_year = None
            self.analysis_final_year = 2020
            self.logfile_prefix = 'o2log_'
            self.logfilename = ''
            self.consumer_calc_generalized_cost = None
            self.policy_targets_file = path + 'proposal_inputs/ghg_standards-footprint_yoy_a_to2032_C_b50_74_m0p35_T_b50_83_m1p38_20221116.csv'
            self.policy_reg_classes_file = path + 'proposal_inputs/regulatory_classes_20210708.csv'
            self.production_multipliers_file = path + 'proposal_inputs/production_multipliers_20230208.csv'
            self.policy_fuels_file = path + 'proposal_inputs/policy_fuels_20220722.csv'
            self.ghg_credit_params_file = path + 'proposal_inputs/ghg_credit_params_20220301.csv'
            self.ghg_credits_file = path + 'proposal_inputs/ghg_credits_21trends_20221122c.csv'
            self.workfactor_definition_file = path + 'proposal_inputs/workfactor_definition_20230106.csv'

            self.context_new_vehicle_market_file = path + 'proposal_inputs/context_new_vehicle_market_20221111.csv'
            self.market_classes_file = path + 'proposal_inputs/market_classes-body_style_20220531.csv'
            self.producer_generalized_cost_file = path + 'proposal_inputs/producer_generalized_cost-body_style_20220613.csv'
            self.production_constraints_file = path + 'proposal_inputs/production_constraints-body_style_20221130.csv'
            self.vehicle_reregistration_file = path + 'proposal_inputs/reregistration_fixed_by_age-body_style_20220531.csv'
            self.sales_share_file = path + 'proposal_inputs/sales_share_params_ice_bev_pu_b0p4_k1p0_x02031-cuv_b2p0_k1p0_x02029_nu8p0-sdn_b0p4_k1p0_x02020_nu1p0_20230228.csv'
            self.required_sales_share_file = path + 'proposal_inputs/required_sales_share-body_style_noACC2_20230222.csv'
            self.onroad_vmt_file = path + 'proposal_inputs/annual_vmt_fixed_by_age-body_style_20221116.csv'
            self.vehicle_price_modifications_file = path + 'proposal_inputs/vehicle_price_modifications_20230314b.csv'

            self.offcycle_credits_file = path + 'proposal_inputs/offcycle_credits_20230206.csv'

            self.consumer_pricing_num_options = 4
            self.consumer_pricing_multiplier_min = 1/1.1
            self.consumer_pricing_multiplier_max = 1.1

            self.new_vehicle_price_elasticity_of_demand = -0.4
            self.timestamp_str = time.strftime('%Y%m%d_%H%M%S')

            self.calc_effects = 'No'  # options are 'No', 'Physical' and 'Physical and Costs' as strings

            # Note that the implicit_price_deflator.csv input file must contain data for this entry:
            self.analysis_dollar_basis = 2020

            self.allow_ice_of_bev = False

            self.ip_deflators_file = path + 'proposal_inputs/implicit_price_deflators_20220104.csv'

            self.start_time = 0
            self.end_time = 0

            # developer settings
            self.producer_market_category_ramp_limit = 0.2
            self.producer_shares_mode = 'auto'
            self.producer_num_market_share_options = 3
            self.producer_num_tech_options_per_ice_vehicle = 3
            self.producer_num_tech_options_per_bev_vehicle = 1
            self.cost_curve_frontier_affinity_factor = 0.75
            self.slice_tech_combo_cloud_tables = False
            self.verbose = False
            self.iterate_producer_consumer = True

            self.footprint_min_scaler = 1 # 1/1.05
            self.footprint_max_scaler = 1 # 1.05
            self.rlhp20_min_scaler = 1.0
            self.rlhp20_max_scaler = 1.0
            self.rlhp60_min_scaler = 1.0
            self.rlhp60_max_scaler = 1.0
            self.producer_voluntary_overcompliance = False  # disable voc by default
            # minimum benefit of overcompliance, as a fraction of compliance cost:
            self.producer_voluntary_overcompliance_min_benefit_frac = 0.01
            self.producer_voluntary_overcompliance_min_strategic_compliance_ratio = 0.9999  # minimal voc by default
            self.producer_price_modification_scaler = 0.0
            self.producer_footprint_wtp = 200
            self.producer_consumer_max_iterations = 5
            self.producer_consumer_convergence_tolerance = 5e-4
            self.producer_compliance_search_min_share_range = 1e-5
            self.producer_compliance_search_convergence_factor = 0.9
            self.producer_compliance_search_tolerance = 1e-6
            self.producer_compliance_search_multipoint = True  # disable for zevregion batches
            self.producer_cross_subsidy_price_tolerance = 5e-3
            self.producer_strategic_compliance_buffer = 0.0
            self.run_profiler = False
            self.multiprocessing = True and not self.run_profiler and not getattr(sys, 'frozen', False)
            self.non_context_session_process_scaler = 1
            self.flat_context = False
            self.flat_context_year = 2021

            self.battery_GWh_limit_years = [2020]
            self.battery_GWh_limit = [1e9]

            self.kwh_per_mile_scale_years = [2020]
            self.kwh_per_mile_scale = [1.0]

            self.redesign_interval_gain_years = [2020, 2029, 2034]
            self.redesign_interval_gain = [0.0, 1.0, 0.0]

            self.manufacturer_gigawatthour_data = None

            # list of modules to allow verbose log files, or empty to disable:
            self.verbose_log_modules = ['database_', 'producer_compliance_search', 'cross_subsidy_search_',
                                        'cv_cost_curves_', 'v_cost_curves_', 'v_cost_clouds_', 'v_cloud_plots_',
                                        'effects_']

            # list of modules to allow verbose console output, or empty to disable
            self.verbose_console_modules = ['producer_compliance_search_',
                                            'p-c_shares_and_costs_', 'p-c_max_iterations_',
                                            'cross_subsidy_search_', 'cross_subsidy_multipliers_',
                                            'cross_subsidy_convergence_']

            self.verbose_postproc = ['iteration_']

            # = 'all' or list of years to log, empty list to disable logging:
            self.log_vehicle_cloud_years = []

            # = 'all' or list of years to log, empty list to disable logging:
            self.log_producer_compliance_search_years = []

            # = 'all' or list of years to log, empty list to disable logging:
            self.log_consumer_iteration_years = [2050]

            # = 'all' or list of years to log, empty list to disable logging:
            self.log_producer_decision_and_response_years = []

            # list of vehicles to plot in log_producer_compliance_search_years:
            self.plot_and_log_vehicles = []  # ['ICE Large Van truck minivan 4WD']

            # dynamic modules / classes
            self.RegulatoryClasses = None
            self.VehicleTargets = None
            self.OffCycleCredits = None
            self.Reregistration = None
            self.OnroadVMT = None
            self.SalesShare = None
            self.ProducerGeneralizedCost = None
            self.MarketClass = None
            self.CostCloud = None

            self.notification_destination = None
            self.notification_email = None
            self.notification_password = None

except:
    print("\n#RUNTIME FAIL\n%s\n" % traceback.format_exc())
    os._exit(-1)
