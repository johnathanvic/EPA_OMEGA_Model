from common import omega_globals, omega_log, TRUE, FALSE
import pandas as pd

'''
Save cost curves for composite vehicles and aggregate (mfr-composite) vehicles into unified dataset
Functions called during compliance search, except for 
industry_cv_cost_curve() does all in one go locally
industry_v_cost_curve() relies on global var to append in eack mfr's complance search, saves in omega.py file

'''

# cv_cost_curve
def industry_cv_cost_curve(calendar_year, compliance_id, candidate_mfr_composite_vehicles):
    industry_cv_df = pd.DataFrame()
    # cv.cost_curve

    # Imported
    for cv in candidate_mfr_composite_vehicles:
        # Line 1141 in vehicles.py
        # if (omega_globals.options.log_vehicle_cloud_years == 'all') or \
        #         (calendar_year in omega_globals.options.log_vehicle_cloud_years):
        #     if 'cv_cost_curves' in omega_globals.options.verbose_log_modules:
        #         filename = '%s%d_%s_%s_cost_curve.csv' % (omega_globals.options.output_folder, cv.model_year,
        #                                                   cv.name.replace(':', '-'), cv.vehicle_id)
        #         cv.cost_curve.to_csv(filename, columns=sorted(cv.cost_curve.columns), index=False)

        # Make pandas
        cv_df = cv.cost_curve.copy()
        cv_df.insert(0, 'compliance_id',compliance_id)
        cv_df.insert(1,'veh_name',cv.name)
        cv_df.insert(2,'market_class',cv.market_class_id)
        cv_df.insert(3,'fueling_class',cv.fueling_class)

        industry_cv_df = industry_cv_df.append(cv_df)

        # Leftoff: writing way to make dataframe appendable by stacking cost_curve df w/ labels, need to figure out how to initilize
    # industry_cv_df.to_csv('industry_cv_df.csv',columns=sorted(industry_cv_df.cost_curve.columns), index=False)        

    industry_cv_df.to_csv('JV_info\industry_cv_df.csv', columns=industry_cv_df.columns[:19],index=False)        # save col up until footprint
    # leftoff: saved cv, now add col for class and powertrain
    return industry_cv_df
    
                
# # v_cost_curve
def industry_v_cost_curve(calendar_year, compliance_id, candidate_mfr_composite_vehicles):
    mfr_df = pd.DataFrame()
    # Imported
    for cv in candidate_mfr_composite_vehicles:

        # Make pandas
        cv_df = cv.cost_curve.copy()
        cv_df.insert(0, 'compliance_id',compliance_id)
        cv_df.insert(1,'veh_name',cv.name)
        cv_df.insert(2,'market_class',cv.market_class_id)
        cv_df.insert(3,'fueling_class',cv.fueling_class)
        # note: add veh identifier number or something
        mfr_df = mfr_df.append(cv_df)

    omega_globals.industry_v_df = omega_globals.industry_v_df.append(mfr_df)

def save_industry_v_cost_curve():
    omega_globals.industry_v_df.to_csv('JV_info\industry_v_df.csv', columns=omega_globals.industry_v_df.columns[:19],index=False) # move to end so not re-saving every automaker

    # before run, need to 
    # ) initilize industry_df
    # ) find how to save (either save in omega.py or note last automaker in omega.py)
    # ) call proper functions


#     # Line 1208 from vehicles.py
#     # if 'v_cost_curves' in omega_globals.options.verbose_log_modules:
#     # filename = '%s%d_%s_%s_cost_curve.csv' % (omega_globals.options.output_folder, self.model_year,
#     #                                             self.name.replace(' ', '_').replace(':', '-'),
#     #                                             self.vehicle_id)
#     # cc = pd.merge(cost_curve, self.cost_curve_non_numeric_data, left_index=True, right_index=True)
#     # cc.to_csv(filename, columns=sorted(cc.columns), index=False)


#     # Issue: trying to find global manufacturer_vehicles
# omega_globals.options.vehicles_df = agg_df

#     '''
#     Notes:
#     Should be able to get aggregate vehicle set in the second iteration
#     '''