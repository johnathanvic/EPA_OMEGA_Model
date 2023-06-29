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
    for vehNo,cv in enumerate(candidate_mfr_composite_vehicles):
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
        cv_df.insert(2,'techOptionNo',vehNo) # techOptionNo
        cv_df.insert(3,'market_class',cv.market_class_id)
        cv_df.insert(4,'fueling_class',cv.fueling_class)
        base_year_market_share = sum(vehicle.base_year_market_share for vehicle in cv.vehicle_list)
        cv_df.insert(5,'base_year_market_share',base_year_market_share)
        cv_df.insert(6,'market_class_share_frac',cv.market_class_share_frac)
        projected_sales = sum(vehicle.projected_sales for vehicle in cv.vehicle_list)
        cv_df.insert(7,'project_sales',projected_sales)
        v_base_year_msrp_dollars = [vehicle.base_year_msrp_dollars for vehicle in cv.vehicle_list]
        base_year_msrp_dollars = sum(v_base_year_msrp_dollars)/len(v_base_year_msrp_dollars)
        cv_df.insert(8,'base_year_msrp_dollars',base_year_msrp_dollars)
        industry_cv_df = industry_cv_df.append(cv_df)

        # Leftoff: writing way to make dataframe appendable by stacking cost_curve df w/ labels, need to figure out how to initilize
    # industry_cv_df.to_csv('industry_cv_df.csv',columns=sorted(industry_cv_df.cost_curve.columns), index=False)        
    last_col = industry_cv_df.columns.get_loc('footprint_ft2')+1
    industry_cv_df = industry_cv_df.iloc[:,:last_col]
    industry_cv_df.to_csv('JV_info\industry_cv_df.csv',index=False)        # save col up until footprint
    # leftoff: saved cv, now add col for class and powertrain
    return industry_cv_df
    
                
# # v_cost_curve
def industry_v_cost_curve(calendar_year, compliance_id, candidate_mfr_composite_vehicles):
    # Construct full industry candidate vehicles by extracting cost curve for each manufacturer's composite candidate vehicle
    # Gets called for each manufacturer & appends to running list omega_globals.industry_v_df, which is initilized in omega.py

    if not omega_globals.industry_v_df.empty: 
        if compliance_id == omega_globals.industry_v_df['compliance_id'].iloc[-1]:
            return # avoid duplicates for same mfr
        
    mfr_df = pd.DataFrame()
    # Iterate through manufacturer's vehicles
    for vehNo,cv in enumerate(candidate_mfr_composite_vehicles):

        # Make dataframe
        cv_df = cv.cost_curve.copy()
        # Declare vehicle id
        veh_id = [compliance_id[:3] +'_'+str(vehNo+1)+'-'+ str(val) for val in range(len(cv_df.index.values))]
        # Add orginization col
        cv_df.insert(0,'compliance_id',compliance_id)
        cv_df.insert(1,'veh_id',veh_id)
        cv_df.insert(2,'veh_name',cv.name)
        cv_df.insert(3,'market_class',cv.market_class_id)
        cv_df.insert(4,'fueling_class',cv.fueling_class)
        cv_df.insert(5,'techNo', cv_df.index.values)
        base_year_market_share = sum(vehicle.base_year_market_share for vehicle in cv.vehicle_list)
        cv_df.insert(6,'base_year_market_share',base_year_market_share)
        cv_df.insert(7,'market_class_share_frac',cv.market_class_share_frac)
        projected_sales = sum(vehicle.projected_sales for vehicle in cv.vehicle_list)
        cv_df.insert(8,'project_sales',projected_sales)
        v_base_year_msrp_dollars = [vehicle.base_year_msrp_dollars for vehicle in cv.vehicle_list]
        base_year_msrp_dollars = sum(v_base_year_msrp_dollars)/len(v_base_year_msrp_dollars)
        cv_df.insert(9,'base_year_msrp_dollars',base_year_msrp_dollars)
        last_col = cv_df.columns.get_loc('footprint_ft2')+1
        mfr_df = mfr_df.append(cv_df.iloc[:,:last_col])

    omega_globals.industry_v_df = omega_globals.industry_v_df.append(mfr_df)

def save_industry_v_cost_curve():
    omega_globals.industry_v_df.to_csv('JV_info\industry_v_df.csv', columns=omega_globals.industry_v_df,index=False) # move to end so not re-saving every automaker
    # omega_globals.industry_v_df.to_csv('JV_info\industry_v_df.csv', columns=omega_globals.industry_v_df.columns[:21],index=False) # move to end so not re-saving every automaker

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